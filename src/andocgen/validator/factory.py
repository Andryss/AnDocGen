from __future__ import annotations

from andocgen.config import ValidationConfig
from andocgen.registry import create_registered
from andocgen.validator.base import DocumentationValidator
from andocgen.validator.implementations.structured import StructuredValidator

_VALIDATORS: dict[str, type[DocumentationValidator]] = {
    "structured": StructuredValidator,
}


def create_validator(config: ValidationConfig) -> DocumentationValidator:
    return create_registered(_VALIDATORS, config.implementation, "validator")
