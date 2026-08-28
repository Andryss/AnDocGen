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


def test_generate_dry_run_does_not_write_reports(tmp_path: Path) -> None:
    out_dir = tmp_path / "docs"
    config_text = MOCK_CONFIG.read_text(encoding="utf-8").replace("./generated_docs", str(out_dir))
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
    assert not out_dir.exists()


def test_init_writes_config_template(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"

    result = runner.invoke(app, ["init", "--output", str(config_path)])

    assert result.exit_code == 0
    assert "config.yaml" in result.stdout
    assert config_path.exists()
    assert "generation:" in config_path.read_text(encoding="utf-8")


def test_inspect_reports_entities_without_output(tmp_path: Path) -> None:
    out_dir = tmp_path / "docs"
    config_text = MOCK_CONFIG.read_text(encoding="utf-8").replace("./generated_docs", str(out_dir))
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    result = runner.invoke(app, ["inspect", str(FIXTURE_PROJECT), "-c", str(config_path)])

    assert result.exit_code == 0
    assert "entities:" in result.stdout
    assert not out_dir.exists()


def test_clean_removes_runtime_directory(tmp_path: Path) -> None:
    out_dir = tmp_path / "docs"
    runtime_dir = out_dir / ".andocgen"
    runtime_dir.mkdir(parents=True)
    config_text = MOCK_CONFIG.read_text(encoding="utf-8").replace("./generated_docs", str(out_dir))
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    result = runner.invoke(app, ["clean", "-c", str(config_path)])

    assert result.exit_code == 0
    assert not runtime_dir.exists()


def test_eval_writes_metrics_reports(tmp_path: Path) -> None:
    out_dir = tmp_path / "docs"
    eval_dir = tmp_path / "eval"
    config_text = MOCK_CONFIG.read_text(encoding="utf-8").replace("./generated_docs", str(out_dir))
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    result = runner.invoke(
        app,
        ["eval", str(FIXTURE_PROJECT), "-c", str(config_path), "--output", str(eval_dir)],
    )

    assert result.exit_code == 0
    assert (eval_dir / "eval_report.json").exists()
    assert (eval_dir / "eval_report.md").exists()
    assert "Entity coverage" in result.stdout
