from __future__ import annotations

import sys
import threading
import time

from andocgen.reporting.progress_format import compute_progress_eta, format_duration_fixed

_ENTITY_WIDTH = 40
_CLEAR_LINE = "\r\033[K"


class ConsoleProgressReporter:
    def __init__(self, quiet: bool = False) -> None:
        self._quiet = quiet
        self._lock = threading.Lock()
        self._start_time: float | None = None
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
            if self._start_time is None:
                self._start_time = time.perf_counter()
            elapsed_sec = time.perf_counter() - self._start_time
            avg_sec, eta_sec = compute_progress_eta(elapsed_sec, current, total)
            line = _format_progress_line(
                current, total, entity_id, ok, avg_sec, eta_sec
            )
            if not self._is_tty:
                print(line, flush=True)
            elif not ok:
                print(f"{_CLEAR_LINE}{line}\n", flush=True)
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
    avg = f"{avg_sec:5.1f}s/ent"
    eta = f"ETA {format_duration_fixed(eta_sec)}"
    return f"{counter} {entity} {status}  {avg}  {eta}"


def _fit_text(text: str, width: int) -> str:
    if len(text) <= width:
        return text.ljust(width)
    if width <= 3:
        return text[:width]
    return text[: width - 3] + "..."
