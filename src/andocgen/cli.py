from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from andocgen.config import AppConfig, load_config
from andocgen.pipeline import run_pipeline
from andocgen.reporting.implementations.console_progress import ConsoleProgressReporter
from andocgen.reporting.implementations.null_progress import NullProgressReporter
from andocgen.reporting.progress_format import format_duration

app = typer.Typer(
    name="andocgen",
    help="Automatic technical documentation generator from source code",
    no_args_is_help=True,
)
config_app = typer.Typer(help="Configuration commands")
app.add_typer(config_app, name="config")

_MAX_ERRORS = 5


def _format_validation_error(exc: ValidationError) -> str:
    lines = ["Configuration validation failed:"]
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"])
        message = error["msg"]
        lines.append(f"  {location}: {message}")
    return "\n".join(lines)


def _load_config_or_exit(config_path: Path | None) -> AppConfig:
    if config_path is None:
        return AppConfig()
    if not config_path.exists():
        print(f"Error: config file not found: {config_path}")
        raise typer.Exit(code=1)
    try:
        return load_config(config_path)
    except ValidationError as exc:
        print(_format_validation_error(exc))
        raise typer.Exit(code=1) from exc


@config_app.command("validate")
def config_validate(
    config_path: Path = typer.Option(..., "--config", "-c", help="Path to config.yaml"),
) -> None:
    """Validate a configuration file against the schema."""
    _load_config_or_exit(config_path)
    print(f"Configuration is valid: {config_path}")


@app.command()
def generate(
    project_path: Path = typer.Argument(..., help="Path to the project directory"),
    config_path: Path | None = typer.Option(
        None, "--config", "-c", help="Path to config.yaml"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Scan, parse, and build call graph without LLM generation",
    ),
) -> None:
    """Generate documentation for a Python project."""
    config = _load_config_or_exit(config_path)
    if not project_path.is_dir():
        print(f"Error: {project_path} is not a directory")
        raise typer.Exit(code=1)

    quiet = config.reporting.quiet
    progress = NullProgressReporter() if quiet else ConsoleProgressReporter()
    result = run_pipeline(project_path, config, progress=progress, dry_run=dry_run)

    if not quiet:
        print()
        print(f"Done in {format_duration(result.elapsed_seconds)}")
        if dry_run:
            print(f"  dry-run entities: {result.dry_run_entities}")
        print(f"  files: {len(result.processed_files)} processed", end="")
        if result.skipped_files:
            print(f", {len(result.skipped_files)} skipped", end="")
        print()
        if result.output_files:
            out_dir = Path(result.output_files[0]).parent
            print(f"  output: {out_dir}")
        print(
            f"  errors: parse {len(result.parse_errors)} | "
            f"generation {len(result.generation_errors)} | "
            f"validation {len(result.errors)}"
        )
        if result.warnings:
            detail = result.detail_log_path or "detail.json"
            print(f"  warnings: {len(result.warnings)} (see {detail})")
        if result.summary_log_path:
            print(f"  logs: {result.summary_log_path}")

        _print_errors("Parse errors", result.parse_errors, lambda e: (e.module_path, e.message))
        _print_errors(
            "Generation errors",
            result.generation_errors,
            lambda e: (
                e.module_path or "-",
                f"{e.entity_type}:{e.entity_name}" if e.entity_name else "-",
                e.message,
            ),
        )
        _print_errors(
            "Validation errors",
            result.errors,
            lambda e: (
                e.module_path,
                f"{e.entity_type}:{e.entity_name}" if e.entity_name else "-",
                e.message,
            ),
        )

    if result.parse_errors or result.generation_errors:
        raise typer.Exit(code=1)


def _print_errors(title: str, items: list, fmt) -> None:
    if not items:
        return
    print(f"\n{title}:")
    for item in items[:_MAX_ERRORS]:
        parts = fmt(item)
        if len(parts) == 2:
            print(f"  {parts[0]}: {parts[1]}")
        else:
            print(f"  {parts[0]} {parts[1]}: {parts[2]}")
    if len(items) > _MAX_ERRORS:
        print(f"  +{len(items) - _MAX_ERRORS} more (see detail.json)")


if __name__ == "__main__":
    app()
