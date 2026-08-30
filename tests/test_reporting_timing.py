from __future__ import annotations

from andocgen.reporting.timing import StageTimer


class _Trace:
    def __init__(self) -> None:
        self.stages: list[tuple[str, str, float | None]] = []

    def log_stage(self, stage: str, detail: str = "", duration_ms: float | None = None) -> None:
        self.stages.append((stage, detail, duration_ms))


def test_stage_timer_logs_start_and_done() -> None:
    trace = _Trace()

    with StageTimer(trace, "scan", "2 files"):
        pass

    assert trace.stages[0] == ("scan", "start 2 files", None)
    assert trace.stages[1][0:2] == ("scan", "done 2 files")
    assert trace.stages[1][2] is not None
