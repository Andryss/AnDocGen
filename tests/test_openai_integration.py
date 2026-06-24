from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from andocgen.config import load_config

from tests.conftest import FIXTURES


def _openai_fixture_configs() -> list[Path]:
    configs: list[Path] = []
    for path in sorted(FIXTURES.glob("config.*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if raw.get("generation", {}).get("provider") == "openai":
            configs.append(path)
    return configs


OPENAI_CONFIGS = _openai_fixture_configs()


@pytest.mark.parametrize("config_path", OPENAI_CONFIGS, ids=lambda p: p.stem)
def test_openai_config_loads_provider_fields(config_path: Path) -> None:
    config = load_config(config_path)
    openai_cfg = config.generation.openai
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    expected = raw["generation"]["providers"]["openai"]

    assert config.generation.provider == "openai"
    assert openai_cfg.base_url == expected["base_url"]
    assert openai_cfg.api_key_env == expected["api_key_env"]
    assert openai_cfg.model == expected["model"]
    assert openai_cfg.project == expected.get("project", "")
    assert openai_cfg.timeout == expected.get("timeout", 120.0)
    assert openai_cfg.temperature == expected.get("temperature")
    assert openai_cfg.max_tokens == expected.get("max_tokens")
