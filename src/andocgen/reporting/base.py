from __future__ import annotations

from typing import Protocol

from andocgen.config import AppConfig
from andocgen.models.entities import PipelineResult


class TraceLogger(Protocol):
    def info(self, message: str) -> None:
        ...

    def debug(self, message: str) -> None:
        ...

    def error(self, message: str) -> None:
        ...

    def log_stage(self, stage: str, detail: str = "", duration_ms: float | None = None) -> None:
        ...

    def log_llm_request(self, entity_id: str, system: str, user: str) -> None:
        ...

    def log_llm_response(
        self, entity_id: str, response: str, duration_ms: float, parsed: bool
    ) -> None:
        ...


class Reporter(Protocol):
    def write_reports(self, result: PipelineResult, config: AppConfig) -> PipelineResult:
        ...

    def create_trace_logger(self, config: AppConfig) -> TraceLogger:
        ...
