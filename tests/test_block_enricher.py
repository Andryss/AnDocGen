from __future__ import annotations

from andocgen.generator.block_enricher import BlockEnricher
from andocgen.generator.section_parser import parse_sections
from andocgen.models.entities import ClassModel, EntityContext, ModuleModel, ParameterModel


def test_enrich_class_fields_from_dataclass_ast() -> None:
    ctx = EntityContext(
        entity_type="class",
        entity_name="Item",
        entity_id="models.py::Item",
        module_path="models.py",
        project_name="demo",
        signature="class Item",
        class_model=ClassModel(
            name="Item",
            is_dataclass=True,
            field_defs=[
                ParameterModel(name="sku", type_annotation="str"),
                ParameterModel(name="title", type_annotation="str"),
                ParameterModel(name="price", type_annotation="float"),
            ],
        ),
    )
    raw = """## Summary

Line item.

## Fields

- `_sku` (`str`) — hallucinated
- `phantom` (`int`) — bad field

## Inheritance

object

## Methods overview

N/A
"""
    block = parse_sections(raw, ctx)
    BlockEnricher().enrich(block, ctx)
    assert block.fields is not None
    assert [field.name for field in block.fields] == ["sku", "title", "price"]
    assert block.inheritance == "N/A"


def test_enrich_plain_class_clears_llm_fields() -> None:
    ctx = EntityContext(
        entity_type="class",
        entity_name="OrderService",
        entity_id="services.py::OrderService",
        module_path="services.py",
        project_name="demo",
        signature="class OrderService",
        class_model=ClassModel(name="OrderService", is_dataclass=False),
    )
    raw = """## Summary

Service class.

## Fields

- `_storage` (`InMemoryStorage`) — private
- `_settings` (`Settings`) — private

## Inheritance

N/A

## Methods overview

N/A
"""
    block = parse_sections(raw, ctx)
    BlockEnricher().enrich(block, ctx)
    assert block.fields == []
