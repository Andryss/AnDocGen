from __future__ import annotations

from andocgen.config import ValidationConfig
from andocgen.validator.base import DocumentationValidator
from andocgen.validator.implementations.structured import StructuredValidator

_VALIDATORS: dict[str, type] = {
    "structured": StructuredValidator,
}


def create_validator(config: ValidationConfig) -> DocumentationValidator:
    impl = config.implementation.lower()
    if impl not in _VALIDATORS:
        raise ValueError(f"Unknown validator implementation: {config.implementation}")
    return _VALIDATORS[impl]()
