from __future__ import annotations

import ast

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
    examples = "\n\n".join(example.code for example in block.examples or [])
    if is_empty_section(examples):
        return []
    fn = ctx.function
    if fn is None:
        return []

    issues: list[RuleIssue] = []
    calls = _parse_example_calls(examples)
    if fn.owner_class and _class_ctor_without_required_args(calls, fn.owner_class, ctx):
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
            if _class_ctor_without_required_args(calls, cls.name, ctx):
                issues.append(
                    RuleIssue(
                        code="examples_invalid_ctor",
                        message=f"Example instantiates `{cls.name}` without constructor arguments",
                    )
                )

    required = _required_params(fn)
    if required and any(call.name == fn.name and call.positional_count == 0 and not call.keywords for call in calls):
        issues.append(
            RuleIssue(
                code="examples_invalid_call",
                message=f"Example calls `{fn.name}()` without required parameters",
            )
        )

    issues.extend(_validate_example_type_names(calls, ctx))
    return issues


def _required_params(fn: FunctionModel) -> list[ParameterModel]:
    return [
        param
        for param in fn.parameters
        if param.name not in ("self", "cls")
        and param.default is None
        and not param.name.startswith("*")
    ]


def _class_ctor_without_required_args(calls: list[_ExampleCall], class_name: str, ctx: EntityContext) -> bool:
    matching_calls = [call for call in calls if call.name == class_name]
    if not matching_calls:
        return False
    cls = _find_class_model(class_name, ctx)
    if cls is None:
        return False
    if cls.is_namedtuple or cls.is_dataclass:
        required_fields = [field for field in cls.field_defs if field.default is None]
        return any(
            call.positional_count == 0 and not (set(call.keywords) & {field.name for field in required_fields})
            for call in matching_calls
        )
    init_fn = _find_class_init(class_name, ctx)
    if init_fn is None:
        return False
    required = _required_params(init_fn)
    return any(call.positional_count < len(required) and not call.keywords for call in matching_calls)


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


def _validate_example_type_names(calls: list[_ExampleCall], ctx: EntityContext) -> list[RuleIssue]:
    module = ctx.module
    if module is None:
        return []
    issues: list[RuleIssue] = []
    for cls in module.classes:
        if (not cls.is_dataclass and not cls.is_namedtuple) or not cls.field_defs:
            continue
        allowed = {field.name for field in cls.field_defs}
        for call in calls:
            if call.name != cls.name:
                continue
            for kw in call.keywords:
                if kw in allowed:
                    continue
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


class _ExampleCall:
    def __init__(self, name: str, positional_count: int, keywords: list[str]) -> None:
        self.name = name
        self.positional_count = positional_count
        self.keywords = keywords


def _parse_example_calls(examples: str) -> list[_ExampleCall]:
    try:
        tree = ast.parse(examples)
    except SyntaxError:
        return []
    calls: list[_ExampleCall] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node.func)
        if not name:
            continue
        calls.append(
            _ExampleCall(
                name=name,
                positional_count=len(node.args),
                keywords=[kw.arg for kw in node.keywords if kw.arg],
            )
        )
    return calls


def _call_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""
