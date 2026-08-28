from __future__ import annotations

import shutil
from pathlib import Path

from andocgen.config import load_config
from andocgen.pipeline import run_pipeline
from tests.conftest import FIXTURE_PROJECT_API, FIXTURE_PROJECT_INCREMENTAL_CALLERS, FIXTURES

MOCK_CONFIG = FIXTURES / "config.mock.yaml"


def test_incremental_skips_unchanged_and_parses_all_modules(tmp_path: Path) -> None:
    config = load_config(MOCK_CONFIG)
    out_dir = tmp_path / "docs"
    config.output.directory = str(out_dir)
    config.generation.incremental = True

    first = run_pipeline(FIXTURE_PROJECT_API, config)
    assert not first.parse_errors
    assert not first.generation_errors
    assert len(first.processed_files) == 3
    assert set(first.processed_files) == {"__init__.py", "handlers.py", "storage.py"}

    second = run_pipeline(FIXTURE_PROJECT_API, config)
    assert not second.parse_errors
    assert not second.generation_errors
    assert second.processed_files == []
    assert set(second.skipped_files) == {"__init__.py", "handlers.py", "storage.py"}
    assert second.dry_run_entities == 0


def test_incremental_regenerates_only_changed_module(tmp_path: Path) -> None:
    config = load_config(MOCK_CONFIG)
    out_dir = tmp_path / "docs"
    config.output.directory = str(out_dir)
    config.generation.incremental = True

    run_pipeline(FIXTURE_PROJECT_API, config)

    handlers_path = FIXTURE_PROJECT_API / "handlers.py"
    original = handlers_path.read_text(encoding="utf-8")
    handlers_path.write_text(original + "\n# touch\n", encoding="utf-8")
    try:
        result = run_pipeline(FIXTURE_PROJECT_API, config)
        assert not result.parse_errors
        assert not result.generation_errors
        assert result.processed_files == ["handlers.py"]
        assert set(result.skipped_files) == {"__init__.py", "storage.py"}
    finally:
        handlers_path.write_text(original, encoding="utf-8")


def test_incremental_regenerates_callers_of_changed_entities(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    shutil.copytree(FIXTURE_PROJECT_INCREMENTAL_CALLERS / "v1", project_dir)
    config = load_config(MOCK_CONFIG)
    config.output.directory = str(tmp_path / "docs")
    config.generation.incremental = True

    first = run_pipeline(project_dir, config)
    assert not first.generation_errors
    assert set(first.processed_files) == {"handlers.py", "storage.py"}

    shutil.copyfile(FIXTURE_PROJECT_INCREMENTAL_CALLERS / "v2" / "storage.py", project_dir / "storage.py")

    second = run_pipeline(project_dir, config)

    assert not second.generation_errors
    assert set(second.processed_files) == {"handlers.py", "storage.py"}
    assert second.skipped_files == []
