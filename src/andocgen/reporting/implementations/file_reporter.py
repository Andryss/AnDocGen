from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from andocgen.config import AppConfig
from andocgen.models.entities import PipelineResult


class FileTraceLogger:
    def __init__(
        self,
        log_path: Path,
        log_llm_content: bool = True,
        max_chars: int = 12000,
    ) -> None:
        self.log_path = log_path
        self.log_llm_content = log_llm_content
        self.max_chars = max_chars
        log_path.parent.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger(f"andocgen.trace.{id(self)}")
        self._logger.handlers.clear()
        self._logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        self._logger.addHandler(handler)
        self._logger.propagate = False

    def info(self, message: str) -> None:
        self._logger.info(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def log_stage(self, stage: str, detail: str = "", duration_ms: float | None = None) -> None:
        parts = [f"[{stage}]"]
        if detail:
            parts.append(detail)
        if duration_ms is not None:
            parts.append(f"({duration_ms:.0f}ms)")
        self._logger.info(" ".join(parts))

    def log_llm_request(self, entity_id: str, system: str, user: str) -> None:
        self._logger.info(
            f"LLM request entity={entity_id} system_chars={len(system)} user_chars={len(user)}"
        )
        if not self.log_llm_content:
            return
        self._log_llm_block(
            entity_id,
            "request",
            [
                ("system prompt", system),
                ("user prompt", user),
            ],
        )

    def log_llm_response(
        self, entity_id: str, response: str, duration_ms: float, parsed: bool
    ) -> None:
        status = "parsed" if parsed else "parse_failed"
        self._logger.info(
            f"LLM response entity={entity_id} status={status} "
            f"chars={len(response)} duration_ms={duration_ms:.0f}"
        )
        if not self.log_llm_content:
            return
        self._log_llm_block(
            entity_id,
            f"response ({status}, {duration_ms:.0f}ms)",
            [("response", response)],
        )

    def _trunc(self, text: str) -> str:
        if len(text) <= self.max_chars:
            return text
        half = self.max_chars // 2
        return (
            f"{text[:half]}\n... [truncated {len(text) - self.max_chars} chars] ...\n{text[-half:]}"
        )

    def _log_llm_block(
        self, entity_id: str, kind: str, sections: list[tuple[str, str]]
    ) -> None:
        lines = [f"LLM {kind} entity={entity_id}"]
        for title, body in sections:
            lines.append(f"--- {title} ---")
            lines.append(self._trunc(body))
        self._logger.debug("\n".join(lines))


class FileReporter:
    def write_reports(self, result: PipelineResult, config: AppConfig) -> PipelineResult:
        logs_dir = config.resolve_logs_dir()
        logs_dir.mkdir(parents=True, exist_ok=True)

        summary_path = logs_dir / config.reporting.summary_file
        detail_path = logs_dir / config.reporting.detail_file
        trace_path = logs_dir / config.reporting.trace_file

        summary_text = (
            f"AnDocGen run summary\n"
            f"Timestamp: {datetime.now().isoformat()}\n"
            f"Processed files: {len(result.processed_files)}\n"
            f"Skipped files: {len(result.skipped_files)}\n"
            f"Parse errors: {len(result.parse_errors)}\n"
            f"Generation errors: {len(result.generation_errors)}\n"
            f"Validation warnings: {len(result.warnings)}\n"
            f"Validation errors: {len(result.errors)}\n"
            f"Output files: {len(result.output_files)}\n"
            f"Elapsed seconds: {result.elapsed_seconds:.2f}\n"
            f"\nLog files:\n"
            f"  trace: {trace_path}\n"
            f"  detail: {detail_path}\n"
        )
        summary_path.write_text(summary_text, encoding="utf-8")

        detail_payload = {
            "parse_errors": [asdict(e) for e in result.parse_errors],
            "generation_errors": [asdict(e) for e in result.generation_errors],
            "validation_issues": [
                {
                    "level": i.level.value,
                    "category": i.category.value,
                    "message": i.message,
                    "module_path": i.module_path,
                    "entity_type": i.entity_type,
                    "entity_name": i.entity_name,
                }
                for i in result.issues
            ],
        }
        detail_path.write_text(
            json.dumps(detail_payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        result.summary_log_path = str(summary_path)
        result.detail_log_path = str(detail_path)
        result.trace_log_path = str(trace_path)
        return result

    def create_trace_logger(self, config: AppConfig) -> FileTraceLogger:
        logs_dir = config.resolve_logs_dir()
        return FileTraceLogger(
            log_path=logs_dir / config.reporting.trace_file,
            log_llm_content=config.reporting.log_llm_content,
            max_chars=config.reporting.trace_max_chars,
        )


class StageTimer:
    def __init__(self, trace: FileTraceLogger, stage: str, detail: str = "") -> None:
        self._trace = trace
        self._stage = stage
        self._detail = detail
        self._start = time.perf_counter()

    def __enter__(self) -> "StageTimer":
        self._trace.log_stage(self._stage, f"start {self._detail}".strip())
        return self

    def __exit__(self, *args: object) -> None:
        elapsed_ms = (time.perf_counter() - self._start) * 1000
        self._trace.log_stage(self._stage, f"done {self._detail}".strip(), elapsed_ms)
