from __future__ import annotations

import ast
from dataclasses import asdict, dataclass
from pathlib import Path

from andocgen.io.json_utils import write_json
from andocgen.models.entities import DocBlock, PipelineResult


@dataclass
class GenerationMetrics:
    total_entities: int
    generated_entities: int
    failed_entities: int
    fallback_entities: int
    parse_errors: int
    generation_errors: int
    validation_warnings: int
    validation_errors: int
    language_mismatch_count: int
    short_summary_count: int
    na_sections_count: int
    examples_count: int
    parseable_examples_count: int
    elapsed_ms_per_entity: float


@dataclass
class EvalReport:
    total_entities: int
    generated_entities: int
    entity_coverage: float
    generation_success_rate: float
    fallback_rate: float
    validation_warnings: int
    validation_errors: int
    language_mismatch_rate: float
    parseable_examples_rate: float
    elapsed_ms_per_entity: float
    metrics: GenerationMetrics


def build_generation_metrics(
    result: PipelineResult,
    *,
    total_entities: int,
    blocks: list[DocBlock] | None = None,
) -> GenerationMetrics:
    blocks = blocks or []
    denominator = max(total_entities, 1)
    generated_entities = len(blocks)
    fallback_count = sum(1 for block in blocks if block.fallback)
    if not fallback_count:
        fallback_count = sum(1 for issue in result.issues if issue.message == "fallback_generated")
    language_mismatches = sum(
        1
        for issue in result.issues
        if "different language" in issue.message or issue.message == "Summary must be in Russian (ru)"
    )
    example_total, example_parseable = _example_parse_counts(blocks)
    return GenerationMetrics(
        total_entities=total_entities,
        generated_entities=generated_entities,
        failed_entities=len(result.generation_errors),
        fallback_entities=fallback_count,
        parse_errors=len(result.parse_errors),
        generation_errors=len(result.generation_errors),
        validation_warnings=len(result.warnings),
        validation_errors=len(result.errors),
        language_mismatch_count=language_mismatches,
        short_summary_count=sum(1 for block in blocks if 0 < len(block.summary.strip()) < 10),
        na_sections_count=_na_sections_count(blocks),
        examples_count=example_total,
        parseable_examples_count=example_parseable,
        elapsed_ms_per_entity=(result.elapsed_seconds * 1000) / denominator,
    )


def build_eval_report(
    result: PipelineResult,
    *,
    total_entities: int,
    blocks: list[DocBlock] | None = None,
) -> EvalReport:
    metrics = build_generation_metrics(result, total_entities=total_entities, blocks=blocks)
    denominator = max(total_entities, 1)

    return EvalReport(
        total_entities=metrics.total_entities,
        generated_entities=metrics.generated_entities,
        entity_coverage=metrics.generated_entities / denominator,
        generation_success_rate=(metrics.total_entities - metrics.failed_entities) / denominator,
        fallback_rate=metrics.fallback_entities / denominator,
        validation_warnings=metrics.validation_warnings,
        validation_errors=metrics.validation_errors,
        language_mismatch_rate=metrics.language_mismatch_count / denominator,
        parseable_examples_rate=(
            metrics.parseable_examples_count / metrics.examples_count
            if metrics.examples_count
            else 1.0
        ),
        elapsed_ms_per_entity=metrics.elapsed_ms_per_entity,
        metrics=metrics,
    )


def render_eval_summary(report: EvalReport) -> str:
    return "\n".join(
        [
            "# AnDocGen Eval Report",
            "",
            f"- Entity coverage: {_pct(report.entity_coverage)} ({report.generated_entities}/{report.total_entities})",
            f"- Generation success rate: {_pct(report.generation_success_rate)}",
            f"- Fallback rate: {_pct(report.fallback_rate)}",
            f"- Validation warnings: {report.validation_warnings}",
            f"- Validation errors: {report.validation_errors}",
            f"- Language mismatch rate: {_pct(report.language_mismatch_rate)}",
            f"- Parseable examples rate: {_pct(report.parseable_examples_rate)}",
            f"- Elapsed per entity: {report.elapsed_ms_per_entity:.0f} ms",
            "",
        ]
    )


def write_eval_report(
    report: EvalReport,
    output_dir: Path,
    *,
    json_name: str = "eval_report.json",
    markdown_name: str = "eval_report.md",
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / json_name
    markdown_path = output_dir / markdown_name
    write_json(json_path, asdict(report))
    markdown_path.write_text(render_eval_summary(report), encoding="utf-8")
    return json_path, markdown_path


def _example_parse_counts(blocks: list[DocBlock]) -> tuple[int, int]:
    total = 0
    parseable = 0
    for block in blocks:
        for example in block.examples or []:
            if example.language.lower() not in ("python", "py"):
                continue
            code = example.code
            total += 1
            try:
                ast.parse(code)
            except SyntaxError:
                continue
            parseable += 1
    return total, parseable


def _na_sections_count(blocks: list[DocBlock]) -> int:
    fields = ("summary", "raises", "edge_cases", "side_effects", "see_also", "inheritance", "methods_overview")
    count = 0
    for block in blocks:
        for field in fields:
            if getattr(block, field, None) == "N/A":
                count += 1
    return count


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"
