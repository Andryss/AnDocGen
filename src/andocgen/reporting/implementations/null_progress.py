from __future__ import annotations


class NullProgressReporter:
    def on_stage(self, message: str) -> None:
        pass

    def on_llm_progress(
        self,
        current: int,
        total: int,
        entity_id: str,
        duration_ms: float,
        ok: bool,
    ) -> None:
        pass
