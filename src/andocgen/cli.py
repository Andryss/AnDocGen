from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from andocgen.config import load_config
from andocgen.pipeline import run_pipeline
from andocgen.reporting.implementations.console_progress import ConsoleProgressReporter
from andocgen.reporting.implementations.null_progress import NullProgressReporter
from andocgen.reporting.progress_format import format_duration

app = typer.Typer(
    name="andocgen",
    help="Automatic technical documentation generator from source code",
    no_args_is_help=True,
)

_MAX_ERRORS = 5


@app.command()
def generate(
    project_path: Path = typer.Argument(..., help="Path to the project directory"),
    config_path: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Path to config.yaml"
    ),
) -> None:
    """Generate documentation for a Python project."""
    config = load_config(config_path)
    if not project_path.is_dir():
        print(f"Error: {project_path} is not a directory")
        raise typer.Exit(code=1)

    quiet = config.reporting.quiet
    progress = NullProgressReporter() if quiet else ConsoleProgressReporter()
    result = run_pipeline(project_path, config, progress=progress)

    if not quiet:
        print()
        print(f"Done in {format_duration(result.elapsed_seconds)}")
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
