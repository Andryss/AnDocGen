from __future__ import annotations

from typing import Protocol

from andocgen.config import GenerationConfig


class LLMProvider(Protocol):
    def complete(self, system: str, user: str) -> str:
        ...
