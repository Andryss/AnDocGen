from __future__ import annotations

import re
from dataclasses import dataclass

from andocgen.generator.formatter import is_empty_section
from andocgen.models.entities import (
    ClassModel,
    DocBlock,
    EntityContext,
    FunctionModel,
    ParameterModel,
)


@dataclass(frozen=True)
class BlockingIssue:
    code: str
    message: str


def validate_summary_language(block: DocBlock, ctx: EntityContext) -> list[BlockingIssue]:
    if ctx.output_language != "ru" or not block.summary.strip():
        return []
    if not _mostly_latin(block.summary):
        return []
    return [
        BlockingIssue(
            code="language_mismatch",
            message="Summary must be in Russian (ru)",
        )
    ]


def _mostly_latin(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 25:
        return False
    if re.search(r"[а-яА-ЯёЁ]", stripped):
        return False
    letters = [char for char in stripped if char.isalpha()]
    if len(letters) < 12:
        return False
    latin = sum(1 for char in letters if ord(char) < 128)
    return latin / len(letters) > 0.5


def validate_entity(block: DocBlock, ctx: EntityContext) -> list[BlockingIssue]:
    issues: list[BlockingIssue] = []
    if block.entity_type in ("function", "method") and ctx.function:
        issues.extend(_validate_phantom_params(block, ctx))
        issues.extend(_validate_examples(block, ctx))
    return issues


def _validate_phantom_params(block: DocBlock, ctx: EntityContext) -> list[BlockingIssue]:
    fn = ctx.function
    assert fn is not None
    param_names = [p.name for p in fn.parameters if p.name not in ("self", "cls")]
    issues: list[BlockingIssue] = []
    for doc_param in block.parameters or []:
        if doc_param.name not in param_names and not doc_param.name.startswith("*"):
            issues.append(
                BlockingIssue(
                    code="phantom_param",
                    message=f"Parameter `{doc_param.name}` does not exist",
                )
            )
    return issues


def _validate_examples(block: DocBlock, ctx: EntityContext) -> list[BlockingIssue]:
    examples = block.examples or ""
    if is_empty_section(examples):
        return []
    fn = ctx.function
    if fn is None:
        return []

    issues: list[BlockingIssue] = []
    if fn.owner_class and _class_ctor_without_required_args(examples, fn.owner_class, ctx):
        issues.append(
            BlockingIssue(
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
                    BlockingIssue(
                        code="examples_invalid_ctor",
                        message=f"Example instantiates `{cls.name}` without constructor arguments",
                    )
                )

    required = _required_params(fn)
    if required and re.search(rf"\b{re.escape(fn.name)}\s*\(\s*\)", examples):
        issues.append(
            BlockingIssue(
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


def _validate_example_type_names(examples: str, ctx: EntityContext) -> list[BlockingIssue]:
    module = ctx.module
    if module is None:
        return []
    issues: list[BlockingIssue] = []
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
                        BlockingIssue(
                            code="examples_invalid_type",
                            message=(
                                f"Example uses unknown field `{kw}` for `{cls.name}` "
                                f"(expected: {', '.join(sorted(allowed))})"
                            ),
                        )
                    )
    return issues


def format_blocking_retry_prompt(issues: list[BlockingIssue]) -> str:
    lines = ["Previous response failed validation:"]
    for issue in issues:
        lines.append(f"- {issue.message}")
    lines.append("")
    if any(issue.code == "language_mismatch" for issue in issues):
        lines.append("Write Summary in the configured output language.")
    else:
        lines.append("Fix Examples to match signatures. Use N/A for Examples if unsure.")
    return "\n".join(lines)
