from __future__ import annotations

import pytest

from andocgen.generator.section_parser import SectionParseError, parse_sections
from andocgen.models.entities import EntityContext


def _ctx(entity_type: str = "function") -> EntityContext:
    return EntityContext(
        entity_type=entity_type,  # type: ignore[arg-type]
        entity_name="add",
        entity_id="calc.py::add",
        module_path="calc.py",
        project_name="demo",
        signature="def add(a: float, b: float) -> float",
    )


def test_parse_valid_function_response() -> None:
    raw = """
{
  "summary": "Adds numbers.",
  "parameters": [
    {"name": "a", "type": "float", "description": "first operand"},
    {"name": "b", "type": "float", "description": "second operand"}
  ],
  "returns": {"type": "float", "description": "sum"},
  "raises": "N/A",
  "edge_cases": "N/A",
  "side_effects": "N/A",
  "examples": [],
  "see_also": "N/A"
}
"""
    block = parse_sections(raw, _ctx())
    assert block.summary == "Adds numbers."
    assert block.parameters is not None
    assert len(block.parameters) == 2
    assert block.returns is not None
    assert block.returns.type == "float"


def test_parse_missing_section_raises() -> None:
    raw = '{"summary": "Only summary."}'
    with pytest.raises(SectionParseError):
        parse_sections(raw, _ctx())


def test_parse_json_parameters_with_optional_metadata() -> None:
    raw = """
{
  "summary": "Adds numbers.",
  "parameters": [
    {"name": "a", "type": "float", "description": "first operand", "optional": false},
    {"name": "b", "type": "float", "description": "second operand", "optional": true, "default": "0"}
  ],
  "returns": {"type": "float", "description": "sum of operands"},
  "raises": "N/A",
  "edge_cases": "N/A",
  "side_effects": "N/A",
  "examples": [],
  "see_also": "N/A"
}
"""
    block = parse_sections(raw, _ctx())
    assert len(block.parameters or []) == 2
    assert block.parameters[0].name == "a"
    assert block.parameters[0].type == "float"
    assert block.parameters[1].optional is True
    assert block.parameters[1].default == "0"
    assert block.returns is not None
    assert block.returns.type == "float"


def test_parse_na_with_extra_text_treated_as_empty() -> None:
    raw = """
{
  "summary": "Adds numbers.",
  "parameters": [{"name": "a", "type": "float", "description": "first operand"}],
  "returns": {"type": "float", "description": "sum"},
  "raises": "N/A — no exceptions",
  "edge_cases": "N/A",
  "side_effects": "N/A",
  "examples": [],
  "see_also": "N/A"
}
"""
    block = parse_sections(raw, _ctx())
    assert block.raises == "N/A"
    assert block.edge_cases == "N/A"


def test_enrich_parameters_from_context() -> None:
    from andocgen.generator.block_enricher import BlockEnricher
    from andocgen.models.entities import FunctionModel, ParameterModel

    ctx = EntityContext(
        entity_type="function",
        entity_name="add",
        entity_id="calc.py::add",
        module_path="calc.py",
        project_name="demo",
        signature="def add(a: float, b: float) -> float",
        function=FunctionModel(
            name="add",
            parameters=[
                ParameterModel(name="a", type_annotation="float"),
                ParameterModel(name="b", type_annotation="float"),
            ],
            returns="float",
        ),
    )
    raw = """
{
  "summary": "Adds numbers.",
  "parameters": [],
  "returns": null,
  "raises": "N/A",
  "edge_cases": "N/A",
  "side_effects": "N/A",
  "examples": [],
  "see_also": "N/A"
}
"""
    block = parse_sections(raw, ctx)
    BlockEnricher().enrich(block, ctx)
    assert len(block.parameters or []) == 2
    assert {p.name for p in block.parameters} == {"a", "b"}
    assert block.returns is not None
    assert block.returns.type == "float"


def test_module_exports_only_from_ast_all() -> None:
    from andocgen.generator.block_enricher import BlockEnricher
    from andocgen.models.entities import ModuleModel

    raw = """
{
  "summary": "Service module.",
  "exports": [
    {"name": "OrderService", "type": "class", "description": "fake export from LLM"}
  ]
}
"""
    ctx = EntityContext(
        entity_type="module",
        entity_name="services.py",
        entity_id="services.py::module",
        module_path="services.py",
        project_name="demo",
        signature="",
        module=ModuleModel(path="services.py", exports=[]),
    )
    block = parse_sections(raw, ctx)
    BlockEnricher().enrich(block, ctx)
    assert block.exports == []

    ctx.module.exports = ["OrderService", "main"]
    block = parse_sections(raw, ctx)
    BlockEnricher().enrich(block, ctx)
    assert block.exports is not None
    assert [e.name for e in block.exports] == ["OrderService", "main"]


def test_module_exports_merge_llm_descriptions() -> None:
    from andocgen.generator.block_enricher import BlockEnricher
    from andocgen.models.entities import ModuleModel

    raw = """
{
  "summary": "Public API.",
  "exports": [
    {"name": "Item", "type": "class", "description": "модель позиции"},
    {"name": "Order", "type": "class", "description": "модель заказа"},
    {"name": "OrderService", "type": "class", "description": "fake, not in __all__"}
  ]
}
"""
    ctx = EntityContext(
        entity_type="module",
        entity_name="__init__.py",
        entity_id="__init__.py::module",
        module_path="__init__.py",
        project_name="demo",
        signature="",
        module=ModuleModel(path="__init__.py", exports=["Item", "Order"]),
    )
    block = parse_sections(raw, ctx)
    BlockEnricher().enrich(block, ctx)
    assert len(block.exports or []) == 2
    by_name = {export.name: export for export in block.exports or []}
    assert by_name["Item"].description == "модель позиции"
    assert by_name["Order"].type == "class"
    assert "OrderService" not in by_name
