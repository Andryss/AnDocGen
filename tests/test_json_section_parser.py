from __future__ import annotations

import pytest

from andocgen.context.implementations.sectioned_prompt import SectionedPromptBuilder
from andocgen.generator.section_parser import SectionParseError, parse_sections
from andocgen.llm.providers.mock import MockProvider
from andocgen.models.entities import EntityContext


def _function_ctx() -> EntityContext:
    return EntityContext(
        entity_type="function",
        entity_name="add",
        entity_id="calc.py::add",
        module_path="calc.py",
        project_name="demo",
        signature="def add(a: int, b: int) -> int",
    )


def test_parse_sections_accepts_json_docblock() -> None:
    raw = """
{
  "summary": "Складывает два числа.",
  "parameters": [
    {"name": "a", "type": "int", "description": "первое число"},
    {"name": "b", "type": "int", "description": "второе число"}
  ],
  "returns": {"type": "int", "description": "сумма"},
  "raises": "N/A",
  "edge_cases": "N/A",
  "side_effects": "N/A",
  "examples": "N/A",
  "see_also": "N/A"
}
"""
    block = parse_sections(raw, _function_ctx())

    assert block.summary == "Складывает два числа."
    assert [p.name for p in block.parameters or []] == ["a", "b"]
    assert block.returns is not None
    assert block.returns.type == "int"


def test_parse_sections_rejects_json_with_unknown_fields() -> None:
    raw = """
{
  "summary": "Складывает два числа.",
  "parameters": [],
  "returns": null,
  "raises": "N/A",
  "edge_cases": "N/A",
  "side_effects": "N/A",
  "examples": "N/A",
  "see_also": "N/A",
  "extra": "not allowed"
}
"""
    with pytest.raises(SectionParseError, match="Unexpected JSON fields"):
        parse_sections(raw, _function_ctx())


def test_parse_sections_rejects_malformed_json() -> None:
    with pytest.raises(SectionParseError, match="Malformed JSON response"):
        parse_sections('{"summary": }', _function_ctx())


def test_parse_sections_rejects_markdown_response() -> None:
    raw = "## Summary\n\nСкладывает два числа.\n"

    with pytest.raises(SectionParseError, match="JSON"):
        parse_sections(raw, _function_ctx())


def test_prompt_requests_json_contract() -> None:
    system = SectionedPromptBuilder().build_system_message("ru", "function")

    assert "Return a JSON object" in system
    assert '"summary"' in system
    assert "Do not return Markdown headings" in system


def test_mock_provider_returns_json_for_function_prompt() -> None:
    prompt = SectionedPromptBuilder()
    ctx = _function_ctx()
    raw = MockProvider(language="ru").complete(
        prompt.build_system_message("ru", "function"),
        prompt.build_user_message(ctx, 32000),
    )
    block = parse_sections(raw, ctx)

    assert raw.strip().startswith("{")
    assert block.summary
    assert block.parameters is not None
