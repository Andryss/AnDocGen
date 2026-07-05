from __future__ import annotations

from andocgen.models.entities import DocBlock, EntityContext
from andocgen.validation.rules.issue import RuleIssue


def validate_phantom_params(block: DocBlock, ctx: EntityContext) -> list[RuleIssue]:
    fn = ctx.function
    if fn is None:
        return []
    param_names = [p.name for p in fn.parameters if p.name not in ("self", "cls")]
    issues: list[RuleIssue] = []
    for doc_param in block.parameters or []:
        if doc_param.name not in param_names and not doc_param.name.startswith("*"):
            issues.append(
                RuleIssue(
                    code="phantom_param",
                    message=f"Parameter `{doc_param.name}` does not exist",
                )
            )
    return issues
