from __future__ import annotations

from andocgen.models.entities import DocBlock, EntityContext
from andocgen.validation.rules.entity_rules import (
    format_blocking_retry_prompt,
    validate_entity_examples,
    validate_summary_language,
)
from andocgen.validation.rules.issue import RuleIssue as BlockingIssue

__all__ = [
    "BlockingIssue",
    "format_blocking_retry_prompt",
    "validate_entity",
    "validate_summary_language",
]


def validate_entity(block: DocBlock, ctx: EntityContext) -> list[BlockingIssue]:
    return validate_entity_examples(block, ctx)
