from __future__ import annotations

import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from andocgen.models.entities import DocBlock, PipelineResult


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


def build_eval_report(
    result: PipelineResult,
    *,
    total_entities: int,
    blocks: list[DocBlock] | None = None,
) -> EvalReport:
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

    return EvalReport(
        total_entities=total_entities,
        generated_entities=generated_entities,
        entity_coverage=generated_entities / denominator,
        generation_success_rate=(total_entities - len(result.generation_errors)) / denominator,
        fallback_rate=fallback_count / denominator,
        validation_warnings=len(result.warnings),
        validation_errors=len(result.errors),
        language_mismatch_rate=language_mismatches / denominator,
        parseable_examples_rate=(example_parseable / example_total) if example_total else 1.0,
        elapsed_ms_per_entity=(result.elapsed_seconds * 1000) / denominator,
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
    json_path.write_text(json.dumps(asdict(report), indent=2, ensure_ascii=False), encoding="utf-8")
    markdown_path.write_text(render_eval_summary(report), encoding="utf-8")
    return json_path, markdown_path


def _example_parse_counts(blocks: list[DocBlock]) -> tuple[int, int]:
    total = 0
    parseable = 0
    for block in blocks:
        for code in _python_code_blocks(block.examples or ""):
            total += 1
            try:
                ast.parse(code)
            except SyntaxError:
                continue
            parseable += 1
    return total, parseable


def _python_code_blocks(markdown: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(r"```(?:python|py)?\s*\n(.*?)```", markdown, re.DOTALL | re.IGNORECASE)
        if match.group(1).strip()
    ]


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"
