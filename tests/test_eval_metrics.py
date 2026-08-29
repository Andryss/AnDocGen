from __future__ import annotations

import json

from andocgen.evaluation.metrics import (
    GenerationMetrics,
    build_eval_report,
    build_generation_metrics,
    render_eval_summary,
    write_eval_report,
)
from andocgen.models.entities import (
    DocBlock,
    ExampleDoc,
    IssueCategory,
    IssueLevel,
    PipelineResult,
    ValidationIssue,
)


def test_build_eval_report_counts_generation_quality_metrics() -> None:
    result = PipelineResult(
        processed_files=["a.py"],
        elapsed_seconds=4.0,
        issues=[
            ValidationIssue(
                level=IssueLevel.WARNING,
                category=IssueCategory.GENERATION,
                message="fallback_generated",
                module_path="a.py",
                entity_type="function",
                entity_name="bad",
            ),
            ValidationIssue(
                level=IssueLevel.WARNING,
                category=IssueCategory.VALIDATION,
                message="Summary appears to be in a different language than configured (ru)",
                module_path="a.py",
                entity_type="function",
                entity_name="bad",
            ),
        ],
    )
    blocks = [
        DocBlock(
            entity_type="function",
            entity_name="ok",
            module_path="a.py",
            summary="Генерирует корректное значение.",
            examples=[ExampleDoc(description="Call ok.", language="python", code="ok()")],
        ),
        DocBlock(
            entity_type="function",
            entity_name="bad",
            module_path="a.py",
            summary="N/A",
            examples=[ExampleDoc(description="Broken call.", language="python", code="bad(")],
            fallback=True,
            fallback_reason="parse error",
        ),
    ]

    report = build_eval_report(result, total_entities=3, blocks=blocks)

    assert report.total_entities == 3
    assert report.generated_entities == 2
    assert report.entity_coverage == 2 / 3
    assert report.generation_success_rate == 1.0
    assert report.fallback_rate == 1 / 3
    assert report.language_mismatch_rate == 1 / 3
    assert report.parseable_examples_rate == 0.5
    assert report.metrics.examples_count == 2
    assert report.metrics.parseable_examples_count == 1
    assert report.metrics.na_sections_count == 1
    assert report.elapsed_ms_per_entity == 4000 / 3
    assert "Entity coverage" in render_eval_summary(report)


def test_build_generation_metrics_returns_dedicated_structure() -> None:
    block = DocBlock(
        entity_type="function",
        entity_name="short",
        module_path="a.py",
        summary="Коротко.",
        examples=[],
    )

    metrics = build_generation_metrics(PipelineResult(elapsed_seconds=2.0), total_entities=1, blocks=[block])

    assert isinstance(metrics, GenerationMetrics)
    assert metrics.generated_entities == 1
    assert metrics.short_summary_count == 1
    assert metrics.examples_count == 0


def test_write_eval_report_saves_json_and_markdown(tmp_path) -> None:
    report = build_eval_report(PipelineResult(elapsed_seconds=1.0), total_entities=1, blocks=[])

    json_path, markdown_path = write_eval_report(report, tmp_path)

    assert json.loads(json_path.read_text(encoding="utf-8"))["total_entities"] == 1
    assert "AnDocGen Eval Report" in markdown_path.read_text(encoding="utf-8")
