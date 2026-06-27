from __future__ import annotations

from pathlib import Path

from andocgen.config import AppConfig, load_config
from andocgen.pipeline import run_pipeline

from tests.conftest import FIXTURE_PROJECT, FIXTURE_PROJECT_LIBRARY, FIXTURES

MOCK_CONFIG = FIXTURES / "config.mock.yaml"


def test_pipeline_fixture_project(tmp_path: Path) -> None:
    config = load_config(MOCK_CONFIG)
    config.output.directory = str(tmp_path / "docs")
    config.reporting.log_llm_content = True

    result = run_pipeline(FIXTURE_PROJECT, config)

    assert not result.parse_errors
    assert not result.generation_errors
    assert (tmp_path / "docs" / "README.md").exists()
    assert (tmp_path / "docs" / "sample.py.md").exists()
    md = (tmp_path / "docs" / "sample.py.md").read_text(encoding="utf-8")
    assert "## Summary" not in md
    assert "### `def greet" in md or "### `greet" in md
    assert (tmp_path / "docs" / ".andocgen" / "logs" / "summary.txt").exists()
    assert (tmp_path / "docs" / ".andocgen" / "logs" / "trace.log").exists()
    trace = (tmp_path / "docs" / ".andocgen" / "logs" / "trace.log").read_text(encoding="utf-8")
    assert "LLM request" in trace
    assert "--- system prompt ---" in trace
    assert "--- response ---" in trace
    assert "## Классы" in md or "## Функции" in md


def test_pipeline_multimodule_mock(tmp_path: Path) -> None:
    config = AppConfig()
    config.output.directory = str(tmp_path / "docs")
    config.generation.provider = "mock"
    config.generation.workers = 4
    config.generation.incremental = False

    result = run_pipeline(FIXTURE_PROJECT_LIBRARY, config)

    assert not result.parse_errors
    assert not result.generation_errors
    assert not result.errors
    assert len(result.warnings) < 10

    services_md = (tmp_path / "docs" / "services.py.md").read_text(encoding="utf-8")
    assert "OrderService" in services_md

    init_md = (tmp_path / "docs" / "__init__.py.md").read_text(encoding="utf-8")
    assert "Экспорт" in init_md or "Exports" in init_md
    assert "OrderService" in init_md or "Item" in init_md
