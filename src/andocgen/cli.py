from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from andocgen.config import load_config
from andocgen.pipeline import run_pipeline

app = typer.Typer(
    name="andocgen",
    help="Automatic technical documentation generator from source code",
    no_args_is_help=True,
)
console = Console()


@app.command("generate")
def generate(
    project_path: Path = typer.Argument(..., help="Path to the project directory"),
    config_path: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Path to config.yaml"
    ),
) -> None:
    """Generate documentation for a Python project."""
    config = load_config(config_path)
    if not project_path.is_dir():
        console.print(f"[red]Error:[/red] {project_path} is not a directory")
        raise typer.Exit(code=1)

    console.print(Panel(f"AnDocGen — generating docs for [bold]{project_path}[/bold]"))
    console.print(f"Provider: [cyan]{config.generation.provider}[/cyan]")

    result = run_pipeline(project_path, config)

    if result.processed_files or result.skipped_files:
        table = Table(title="Files")
        table.add_column("Path")
        table.add_column("Status")
        for path in result.processed_files:
            table.add_row(path, "[green]processed[/green]")
        for path in result.skipped_files:
            table.add_row(path, "[dim]skipped[/dim]")
        console.print(table)

    if result.parse_errors:
        parse_table = Table(title="Parse errors")
        parse_table.add_column("Module")
        parse_table.add_column("Message", style="red")
        for err in result.parse_errors:
            parse_table.add_row(err.module_path, err.message)
        console.print(parse_table)

    if result.generation_errors:
        gen_table = Table(title="Generation errors")
        gen_table.add_column("Module")
        gen_table.add_column("Entity")
        gen_table.add_column("Message", style="red")
        for err in result.generation_errors:
            entity = f"{err.entity_type}:{err.entity_name}" if err.entity_name else "-"
            gen_table.add_row(err.module_path or "-", entity, err.message)
        console.print(gen_table)

    if result.warnings:
        warn_table = Table(title="Validation warnings")
        warn_table.add_column("Module")
        warn_table.add_column("Entity")
        warn_table.add_column("Message", style="yellow")
        for issue in result.warnings:
            entity = f"{issue.entity_type}:{issue.entity_name}" if issue.entity_name else "-"
            warn_table.add_row(issue.module_path, entity, issue.message)
        console.print(warn_table)

    if result.errors:
        err_table = Table(title="Validation errors")
        err_table.add_column("Module")
        err_table.add_column("Entity")
        err_table.add_column("Message", style="red")
        for issue in result.errors:
            entity = f"{issue.entity_type}:{issue.entity_name}" if issue.entity_name else "-"
            err_table.add_row(issue.module_path, entity, issue.message)
        console.print(err_table)

    summary = (
        f"Processed: {len(result.processed_files)} | "
        f"Skipped: {len(result.skipped_files)} | "
        f"Output files: {len(result.output_files)} | "
        f"Parse errors: {len(result.parse_errors)} | "
        f"Generation errors: {len(result.generation_errors)} | "
        f"Warnings: {len(result.warnings)} | "
        f"Errors: {len(result.errors)} | "
        f"Time: {result.elapsed_seconds:.2f}s"
    )
    console.print(Panel(summary, title="Summary", style="bold blue"))

    if result.summary_log_path:
        console.print(f"\nLogs: {result.summary_log_path}")

    if result.output_files:
        console.print("\nOutput:")
        for path in result.output_files:
            console.print(f"  {path}")

    if result.parse_errors or result.generation_errors:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
