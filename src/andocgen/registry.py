from __future__ import annotations

from collections.abc import Mapping
from typing import TypeVar

T = TypeVar("T")


def create_registered(registry: Mapping[str, type[T]], implementation: object, component: str) -> T:
    key = str(implementation or "").lower()
    cls = registry.get(key)
    if cls is None:
        raise ValueError(f"Unknown {component} implementation: {implementation}")
    return cls()
