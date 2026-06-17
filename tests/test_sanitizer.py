from __future__ import annotations

from andocgen.generator.response_sanitizer import normalize_llm_response


def test_strips_markdown_fence() -> None:
    raw = "```markdown\n## Summary\n\nHello\n```"
    assert normalize_llm_response(raw).startswith("## Summary")


def test_strips_plain_fence() -> None:
    raw = "```\n## Summary\n\nHi\n```"
    assert "## Summary" in normalize_llm_response(raw)


def test_preserves_json_without_summary() -> None:
    raw = '{"summary": "narrative"}'
    assert normalize_llm_response(raw) == raw


def test_preserves_normal_sections() -> None:
    raw = "## Summary\n\nText\n\n## Parameters\n\nN/A"
    assert normalize_llm_response(raw) == raw
