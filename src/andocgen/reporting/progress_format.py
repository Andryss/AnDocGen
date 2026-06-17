from __future__ import annotations

import time


def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours}h {minutes}m"


def format_duration_fixed(seconds: float, width: int = 6) -> str:
    return format_duration(seconds).rjust(width)


def compute_progress_eta(elapsed_sec: float, current: int, total: int) -> tuple[float, float]:
    """Average wall-clock seconds per completed entity and ETA for the rest."""
    if current <= 0:
        return 0.0, 0.0
    avg_sec = elapsed_sec / current
    eta_sec = max(0.0, avg_sec * (total - current))
    return avg_sec, eta_sec
