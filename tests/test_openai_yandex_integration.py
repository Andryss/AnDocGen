from __future__ import annotations

import os
from pathlib import Path

import pytest

from andocgen.config import load_config
from andocgen.pipeline import run_pipeline

MINI_API = Path(__file__).resolve().parents[1] / "examples" / "mini_api"
YANDEX_CONFIG = MINI_API / "config.yandex.yaml"


def test_yandex_config_loads_openai_provider_fields() -> None:
    config = load_config(YANDEX_CONFIG)
    openai_cfg = config.generation.openai

    assert config.generation.provider == "openai"
    assert openai_cfg.base_url == "https://ai.api.cloud.yandex.net/v1"
    assert openai_cfg.api_key_env == "YANDEX_API_KEY"
    assert openai_cfg.project == "b1gXXXXXXXX"
    assert openai_cfg.model == "gpt://b1gXXXXXXXX/yandexgpt/latest"
    assert openai_cfg.temperature == 0.3
    assert openai_cfg.max_tokens == 4000


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("YANDEX_API_KEY"),
    reason="YANDEX_API_KEY not set",
)
def test_mini_api_yandex_generation() -> None:
    config = load_config(YANDEX_CONFIG)
    assert config.generation.openai.project
    assert config.generation.openai.project != "b1gXXXXXXXX"

    result = run_pipeline(MINI_API, config)

    assert not result.generation_errors
    assert len(result.processed_files) >= 1
    docs_dir = MINI_API / "generated_docs"
    assert (docs_dir / "handlers.py.md").exists()
    content = (docs_dir / "handlers.py.md").read_text(encoding="utf-8")
    assert len(content.strip()) > 100
