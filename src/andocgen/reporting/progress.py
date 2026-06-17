from __future__ import annotations

from typing import Protocol


class ProgressReporter(Protocol):
    def on_stage(self, message: str) -> None:
        ...

    def on_llm_progress(
        self,
        current: int,
        total: int,
        entity_id: str,
        duration_ms: float,
        ok: bool,
    ) -> None:
        ...
