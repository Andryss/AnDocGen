from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from andocgen.cli import app
from tests.conftest import FIXTURE_PROJECT, FIXTURES

runner = CliRunner()
MOCK_CONFIG = FIXTURES / "config.mock.yaml"


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "generate" in result.stdout


def test_config_validate_success() -> None:
    result = runner.invoke(app, ["config", "validate", "-c", str(MOCK_CONFIG)])
    assert result.exit_code == 0
    assert "valid" in result.stdout.lower()


def test_config_validate_invalid_field(tmp_path: Path) -> None:
    bad_config = tmp_path / "bad.yaml"
    bad_config.write_text(
        "generation:\n  provider: not-a-real-provider\n",
        encoding="utf-8",
    )
    result = runner.invoke(app, ["config", "validate", "-c", str(bad_config)])
    assert result.exit_code == 1
    assert "validation failed" in result.stdout.lower()


def test_generate_dry_run(tmp_path: Path) -> None:
    config_text = MOCK_CONFIG.read_text(encoding="utf-8").replace("quiet: true", "quiet: false")
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_text, encoding="utf-8")
    result = runner.invoke(
        app,
        [
            "generate",
            str(FIXTURE_PROJECT),
            "-c",
            str(config_path),
            "--dry-run",
        ],
    )
    assert result.exit_code == 0
    assert "dry-run entities" in result.stdout
