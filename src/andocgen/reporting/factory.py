from __future__ import annotations

from andocgen.config import ReportingConfig
from andocgen.reporting.base import Reporter
from andocgen.reporting.implementations.file_reporter import FileReporter

_REPORTERS: dict[str, type] = {
    "file": FileReporter,
}


def create_reporter(config: ReportingConfig) -> Reporter:
    impl = config.implementation.lower()
    if impl not in _REPORTERS:
        raise ValueError(f"Unknown reporter implementation: {config.implementation}")
    return _REPORTERS[impl]()
