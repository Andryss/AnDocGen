from __future__ import annotations

import re

from andocgen.generator.formatter import is_empty_section
from andocgen.models.entities import (
    ClassModel,
    DocBlock,
    EntityContext,
    FunctionModel,
    ParameterModel,
)
from andocgen.validation.rules.issue import RuleIssue
from andocgen.validation.rules.phantom_params import validate_phantom_params
from andocgen.validation.rules.text_quality import mostly_latin


def validate_summary_language(block: DocBlock, ctx: EntityContext) -> list[RuleIssue]:
    if ctx.output_language != "ru" or not block.summary.strip():
        return []
    if not mostly_latin(block.summary):
        return []
    return [
        RuleIssue(
            code="language_mismatch",
            message="Summary must be in Russian (ru)",
        )
    ]


def validate_entity_examples(block: DocBlock, ctx: EntityContext) -> list[RuleIssue]:
    if block.entity_type not in ("function", "method") or not ctx.function:
        return []
    issues: list[RuleIssue] = []
    issues.extend(validate_phantom_params(block, ctx))
    issues.extend(_validate_examples(block, ctx))
    return issues


def format_blocking_retry_prompt(issues: list[RuleIssue]) -> str:
    lines = ["Previous response failed validation:"]
    for issue in issues:
        lines.append(f"- {issue.message}")
    lines.append("")
    if any(issue.code == "language_mismatch" for issue in issues):
        lines.append("Write Summary in the configured output language.")
    else:
        lines.append("Fix Examples to match signatures. Use N/A for Examples if unsure.")
    return "\n".join(lines)


def _validate_examples(block: DocBlock, ctx: EntityContext) -> list[RuleIssue]:
    examples = block.examples or ""
    if is_empty_section(examples):
        return []
    fn = ctx.function
    if fn is None:
        return []

    issues: list[RuleIssue] = []
    if fn.owner_class and _class_ctor_without_required_args(examples, fn.owner_class, ctx):
        issues.append(
            RuleIssue(
                code="examples_invalid_ctor",
                message=f"Example instantiates `{fn.owner_class}` without constructor arguments",
            )
        )

    module = ctx.module
    if module is not None:
        for cls in module.classes:
            if fn.owner_class and cls.name == fn.owner_class:
                continue
            if _class_ctor_without_required_args(examples, cls.name, ctx):
                issues.append(
                    RuleIssue(
                        code="examples_invalid_ctor",
                        message=f"Example instantiates `{cls.name}` without constructor arguments",
                    )
                )

    required = _required_params(fn)
    if required and re.search(rf"\b{re.escape(fn.name)}\s*\(\s*\)", examples):
        issues.append(
            RuleIssue(
                code="examples_invalid_call",
                message=f"Example calls `{fn.name}()` without required parameters",
            )
        )

    issues.extend(_validate_example_type_names(examples, ctx))
    return issues


def _required_params(fn: FunctionModel) -> list[ParameterModel]:
    return [
        param
        for param in fn.parameters
        if param.name not in ("self", "cls")
        and param.default is None
        and not param.name.startswith("*")
    ]


def _class_ctor_without_required_args(
    examples: str, class_name: str, ctx: EntityContext
) -> bool:
    if not re.search(rf"\b{re.escape(class_name)}\s*\(\s*\)", examples):
        return False
    cls = _find_class_model(class_name, ctx)
    if cls is None:
        return False
    if cls.is_namedtuple or cls.is_dataclass:
        required_fields = [field for field in cls.field_defs if field.default is None]
        return bool(required_fields)
    init_fn = _find_class_init(class_name, ctx)
    if init_fn is None:
        return False
    return bool(_required_params(init_fn))


def _find_class_init(class_name: str, ctx: EntityContext) -> FunctionModel | None:
    cls = _find_class_model(class_name, ctx)
    if cls is None:
        return None
    for method in cls.methods:
        if method.name == "__init__":
            return method
    return None


def _find_class_model(class_name: str, ctx: EntityContext) -> ClassModel | None:
    if ctx.class_model and ctx.class_model.name == class_name:
        return ctx.class_model
    module = ctx.module
    if module is None:
        return None
    for cls in module.classes:
        if cls.name == class_name:
            return cls
    return None


def _validate_example_type_names(examples: str, ctx: EntityContext) -> list[RuleIssue]:
    module = ctx.module
    if module is None:
        return []
    issues: list[RuleIssue] = []
    for cls in module.classes:
        if (not cls.is_dataclass and not cls.is_namedtuple) or not cls.field_defs:
            continue
        allowed = {field.name for field in cls.field_defs}
        for match in re.finditer(rf"\b{re.escape(cls.name)}\s*\(([^)]*)\)", examples):
            args = match.group(1).strip()
            if not args or "=" not in args:
                continue
            for kw in re.findall(r"(\w+)\s*=", args):
                if kw not in allowed:
                    issues.append(
                        RuleIssue(
                            code="examples_invalid_type",
                            message=(
                                f"Example uses unknown field `{kw}` for `{cls.name}` "
                                f"(expected: {', '.join(sorted(allowed))})"
                            ),
                        )
                    )
    return issues
