from __future__ import annotations

import time

from andocgen.reporting.base import TraceLogger


class StageTimer:
    def __init__(self, trace: TraceLogger, stage: str, detail: str = "") -> None:
        self._trace = trace
        self._stage = stage
        self._detail = detail
        self._start = time.perf_counter()

    def __enter__(self) -> StageTimer:
        self._trace.log_stage(self._stage, f"start {self._detail}".strip())
        return self

    def __exit__(self, *args: object) -> None:
        elapsed_ms = (time.perf_counter() - self._start) * 1000
        self._trace.log_stage(self._stage, f"done {self._detail}".strip(), elapsed_ms)
