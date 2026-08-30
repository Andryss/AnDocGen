from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    def complete(self, system: str, user: str, *, entity_type: str = "function") -> str:
        ...
