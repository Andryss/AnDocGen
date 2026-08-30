from __future__ import annotations

from andocgen.config import ReportingConfig
from andocgen.registry import create_registered
from andocgen.reporting.base import Reporter
from andocgen.reporting.implementations.file_reporter import FileReporter

_REPORTERS: dict[str, type[Reporter]] = {
    "file": FileReporter,
}


def create_reporter(config: ReportingConfig) -> Reporter:
    return create_registered(_REPORTERS, config.implementation, "reporter")
