from __future__ import annotations

from pathlib import Path

from andocgen.config import AppConfig
from andocgen.pipeline import run_pipeline


def test_pipeline_mini_calculator(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    project = root / "examples" / "mini_calculator"
    config = AppConfig()
    config.output.directory = str(tmp_path / "docs")
    config.generation.provider = "mock"
    config.generation.incremental = False

    result = run_pipeline(project, config)

    assert not result.parse_errors
    assert not result.generation_errors
    assert (tmp_path / "docs" / "README.md").exists()
    assert (tmp_path / "docs" / "calculator.py.md").exists()
    md = (tmp_path / "docs" / "calculator.py.md").read_text(encoding="utf-8")
    assert "## Summary" not in md
    assert "### `def add" in md or "### `add" in md
    assert (tmp_path / "docs" / "logs" / "summary.txt").exists()
    assert (tmp_path / "docs" / "logs" / "trace.log").exists()
    trace = (tmp_path / "docs" / "logs" / "trace.log").read_text(encoding="utf-8")
    assert "LLM request" in trace
    assert "--- system prompt ---" in trace
    assert "--- response ---" in trace
    assert "## Классы" in md or "## Функции" in md


def test_pipeline_mini_library_mock(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    project = root / "examples" / "mini_library"
    config = AppConfig()
    config.output.directory = str(tmp_path / "docs")
    config.generation.provider = "mock"
    config.generation.workers = 4
    config.generation.incremental = False

    result = run_pipeline(project, config)

    assert not result.parse_errors
    assert not result.generation_errors
    assert not result.errors
    assert len(result.warnings) < 10

    services_md = (tmp_path / "docs" / "services.py.md").read_text(encoding="utf-8")
    assert "OrderService" in services_md

    init_md = (tmp_path / "docs" / "__init__.py.md").read_text(encoding="utf-8")
    assert "Экспорт" in init_md or "Exports" in init_md
    assert "OrderService" in init_md or "Item" in init_md

