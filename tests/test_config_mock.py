from __future__ import annotations

from pathlib import Path

import yaml

from andocgen.config import load_config
from andocgen.pipeline import run_pipeline

from tests.conftest import FIXTURES, FIXTURE_PROJECT

MOCK_CONFIG = FIXTURES / "config.mock.yaml"


def test_mock_config_loads_expected_fields() -> None:
    config = load_config(MOCK_CONFIG)
    raw = yaml.safe_load(MOCK_CONFIG.read_text(encoding="utf-8")) or {}

    assert config.project.name == raw["project"]["name"]
    assert config.generation.provider == "mock"
    assert config.generation.language == "ru"
    assert config.generation.incremental is False
    assert config.output.format == "markdown"


def test_mock_config_runs_pipeline(tmp_path: Path) -> None:
    config = load_config(MOCK_CONFIG)
    config.output.directory = str(tmp_path / "docs")

    result = run_pipeline(FIXTURE_PROJECT, config)

    assert not result.parse_errors
    assert not result.generation_errors
    assert (tmp_path / "docs" / "sample.py.md").exists()
    assert (tmp_path / "docs" / "logs" / "summary.txt").exists()
