from __future__ import annotations

import sys
import threading

from andocgen.reporting.progress_format import format_duration_fixed

_ENTITY_WIDTH = 40
_CLEAR_LINE = "\r\033[K"


class ConsoleProgressReporter:
    def __init__(self, quiet: bool = False) -> None:
        self._quiet = quiet
        self._lock = threading.Lock()
        self._durations: list[float] = []
        self._is_tty = sys.stdout.isatty()

    def on_stage(self, message: str) -> None:
        if not self._quiet:
            print(message, flush=True)

    def on_llm_progress(
        self,
        current: int,
        total: int,
        entity_id: str,
        duration_ms: float,
        ok: bool,
    ) -> None:
        if self._quiet:
            return
        with self._lock:
            self._durations.append(duration_ms)
            avg_ms = sum(self._durations) / len(self._durations)
            eta_sec = max(0.0, (total - current) * avg_ms / 1000)
            line = _format_progress_line(
                current, total, entity_id, ok, avg_ms / 1000, eta_sec
            )
            if not ok or not self._is_tty:
                print(line, flush=True)
            else:
                print(f"{_CLEAR_LINE}{line}", end="", flush=True)
                if current >= total:
                    print(flush=True)


def _format_progress_line(
    current: int,
    total: int,
    entity_id: str,
    ok: bool,
    avg_sec: float,
    eta_sec: float,
) -> str:
    width = len(str(total))
    counter = f"[{current:>{width}d}/{total}]"
    entity = _fit_text(entity_id, _ENTITY_WIDTH)
    status = "ok  " if ok else "FAIL"
    avg = f"{avg_sec:5.1f}s/req"
    eta = f"ETA {format_duration_fixed(eta_sec)}"
    return f"{counter} {entity} {status}  {avg}  {eta}"


def _fit_text(text: str, width: int) -> str:
    if len(text) <= width:
        return text.ljust(width)
    if width <= 3:
        return text[:width]
    return text[: width - 3] + "..."
