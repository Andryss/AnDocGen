from __future__ import annotations

import json

from andocgen.config import AppConfig
from andocgen.models.entities import PipelineResult
from andocgen.reporting.implementations.file_reporter import FileReporter


def test_llm_trace_writes_content_when_enabled(tmp_path) -> None:
    config = AppConfig()
    config.output.directory = str(tmp_path / "docs")
    config.reporting.log_llm_content = True
    trace = FileReporter().create_trace_logger(config)

    trace.log_llm_attempt(
        entity_id="a.py::add",
        entity_type="function",
        entity_name="add",
        module_path="a.py",
        provider="mock",
        model="mock",
        attempt=0,
        duration_ms=12.0,
        system="system prompt",
        user="user prompt",
        raw_response='{"summary":"ok"}',
        parse_ok=True,
        validation_ok=True,
    )

    lines = (tmp_path / "docs" / ".andocgen" / "logs" / "llm_responses.jsonl").read_text(encoding="utf-8").splitlines()
    payload = json.loads(lines[0])
    assert payload["entity_id"] == "a.py::add"
    assert payload["request"]["system"] == "system prompt"
    assert payload["response"]["raw"] == '{"summary":"ok"}'
    assert payload["parse_ok"] is True


def test_llm_trace_redacts_content_when_disabled(tmp_path) -> None:
    config = AppConfig()
    config.output.directory = str(tmp_path / "docs")
    config.reporting.log_llm_content = False
    trace = FileReporter().create_trace_logger(config)

    trace.log_llm_attempt(
        entity_id="a.py::add",
        entity_type="function",
        entity_name="add",
        module_path="a.py",
        provider="mock",
        model="mock",
        attempt=0,
        duration_ms=12.0,
        system="secret system",
        user="secret user",
        raw_response="secret response",
        parse_ok=False,
        validation_ok=False,
        retry_reason="parse failed",
        fallback_reason="Malformed JSON response",
    )

    payload = json.loads(
        (tmp_path / "docs" / ".andocgen" / "logs" / "llm_responses.jsonl").read_text(encoding="utf-8")
    )
    assert "request" not in payload
    assert "response" not in payload
    assert payload["retry_reason"] == "parse failed"
    assert payload["fallback_reason"] == "Malformed JSON response"


def test_report_summary_includes_fallback_count(tmp_path) -> None:
    config = AppConfig()
    config.output.directory = str(tmp_path / "docs")
    result = PipelineResult()

    FileReporter().write_reports(result, config)

    summary = (tmp_path / "docs" / ".andocgen" / "logs" / "summary.txt").read_text(encoding="utf-8")
    assert "Fallback generated: 0" in summary
