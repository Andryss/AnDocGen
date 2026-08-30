from __future__ import annotations

import ast

from andocgen.models.entities import DocBlock, EntityContext
from andocgen.python.ast_utils import raised_exception_names
from andocgen.text.sections import is_empty_section
from andocgen.validation.rules.issue import RuleIssue
from andocgen.validation.rules.text_quality import mostly_latin


def validate_semantic_consistency(block: DocBlock, ctx: EntityContext) -> list[RuleIssue]:
    if block.entity_type not in ("function", "method") or not ctx.function:
        return []
    fn = ctx.function
    issues: list[RuleIssue] = []
    issues.extend(_validate_raises(block, fn.source_body))
    issues.extend(_validate_side_effects(block, fn.calls))
    issues.extend(_validate_return_type(block, fn.returns))
    issues.extend(_validate_python_examples(block))
    return issues


def validate_text_language(block: DocBlock, ctx: EntityContext) -> list[RuleIssue]:
    if ctx.output_language != "ru":
        return []
    fields = [
        ("summary", block.summary),
        ("raises", block.raises),
        ("edge_cases", block.edge_cases),
        ("side_effects", block.side_effects),
        ("see_also", block.see_also),
        ("purpose", block.purpose),
        ("usage_notes", block.usage_notes),
        ("methods_overview", block.methods_overview),
    ]
    issues: list[RuleIssue] = []
    for name, value in fields:
        if value and not is_empty_section(value) and mostly_latin(value):
            issues.append(
                RuleIssue(
                    code="language_mismatch",
                    message=f"Field `{name}` appears to be in a different language than configured (ru)",
                )
            )
    return issues


def _validate_raises(block: DocBlock, source_body: str) -> list[RuleIssue]:
    raised = raised_exception_names(source_body)
    if not raised or not is_empty_section(block.raises):
        return []
    return [
        RuleIssue(
            code="undocumented_raise",
            message=f"Raised exception `{name}` is not documented",
        )
        for name in sorted(raised)
    ]


def _validate_side_effects(block: DocBlock, calls: list[str]) -> list[RuleIssue]:
    call_names = set(calls)
    has_side_effect = bool(
        call_names
        & {
            "open",
            "Path.write_text",
            "Path.write_bytes",
            "write_text",
            "write_bytes",
            "print",
            "requests.get",
            "requests.post",
            "httpx.get",
            "httpx.post",
        }
    )
    if not has_side_effect or not is_empty_section(block.side_effects):
        return []
    return [
        RuleIssue(
            code="undocumented_side_effect",
            message="Function appears to perform I/O or other side effects but side_effects is empty",
        )
    ]


def _validate_return_type(block: DocBlock, expected: str | None) -> list[RuleIssue]:
    if not expected or expected in ("None", "NoneType"):
        return []
    if not block.returns or not (block.returns.type or block.returns.description):
        return [
            RuleIssue(
                code="return_mismatch",
                message=f"Return type `{expected}` is not documented",
            )
        ]
    actual = (block.returns.type or "").strip()
    if actual and actual not in {expected, f"`{expected}`"}:
        return [
            RuleIssue(
                code="return_mismatch",
                message=f"Return type `{expected}` differs from documented `{actual}`",
            )
        ]
    return []


def _validate_python_examples(block: DocBlock) -> list[RuleIssue]:
    issues: list[RuleIssue] = []
    for example in block.examples or []:
        if example.language.strip().lower() not in ("python", "py"):
            continue
        try:
            ast.parse(example.code)
        except SyntaxError:
            issues.append(
                RuleIssue(
                    code="examples_invalid_python",
                    message="Example code must be valid Python",
                )
            )
    return issues

