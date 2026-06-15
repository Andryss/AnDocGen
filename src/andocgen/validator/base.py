from __future__ import annotations

from typing import Protocol

from andocgen.config import ValidationConfig
from andocgen.models.entities import DocBlock, EntityContext, ValidationIssue


class DocumentationValidator(Protocol):
    def validate(
        self,
        blocks: list[DocBlock],
        contexts: list[EntityContext],
        config: ValidationConfig,
    ) -> list[ValidationIssue]:
        ...
