from __future__ import annotations

from pathlib import Path

from andocgen.config import AppConfig


def test_default_cache_and_logs_dirs(tmp_path: Path) -> None:
    config = AppConfig()
    config.output.directory = str(tmp_path / "out")
    assert config.resolve_cache_dir() == tmp_path / "out" / ".andocgen" / "cache"
    assert config.resolve_logs_dir() == tmp_path / "out" / ".andocgen" / "logs"
