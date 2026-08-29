from __future__ import annotations

from pathlib import Path

from andocgen.config import AppConfig, load_config


def test_default_cache_and_logs_dirs(tmp_path: Path) -> None:
    config = AppConfig()
    config.output.directory = str(tmp_path / "out")
    assert config.resolve_cache_dir() == tmp_path / "out" / ".andocgen" / "cache"
    assert config.resolve_logs_dir() == tmp_path / "out" / ".andocgen" / "logs"


def test_config_paths_resolve_relative_to_config_file(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "config.yaml"
    config_path.write_text(
        """
output:
  directory: ./docs
  cache_path: ./cache
reporting:
  logs_dir: ./logs
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.resolve_output_dir() == config_dir / "docs"
    assert config.resolve_cache_dir() == config_dir / "cache"
    assert config.resolve_logs_dir() == config_dir / "logs"
