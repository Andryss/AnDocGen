from __future__ import annotations

from andocgen.generator.formatter import format_markdown, is_empty_section
from andocgen.models.entities import DocBlock, ParameterDoc, ReturnDoc


def test_format_function_markdown() -> None:
    block = DocBlock(
        entity_type="function",
        entity_name="add",
        module_path="calc.py",
        signature="def add(a: float, b: float) -> float",
        summary="Adds numbers.",
        parameters=[
            ParameterDoc(name="a", type="float", description="first"),
            ParameterDoc(name="b", type="float", description="second"),
        ],
        returns=ReturnDoc(type="float", description="sum"),
    )
    content = format_markdown(block, "ru")
    assert "### `def add(a: float, b: float) -> float`" in content
    assert "**Параметры:**" in content
    assert "`a`" in content
    assert "**Исключения:**" not in content


def test_format_skips_na_optional_sections() -> None:
    block = DocBlock(
        entity_type="function",
        entity_name="add",
        module_path="calc.py",
        signature="def add(a: float, b: float) -> float",
        summary="Adds numbers.",
        parameters=[ParameterDoc(name="a", type="float", description="first")],
        returns=ReturnDoc(type="float", description="sum"),
        raises="N/A",
        edge_cases="N/A — none",
        side_effects="**N/A**",
        examples="N/A",
        see_also="N/A",
    )
    content = format_markdown(block, "ru")
    assert "**Исключения:**" not in content
    assert "**Граничные случаи:**" not in content
    assert "**Побочные эффекты:**" not in content
    assert "**Примеры:**" not in content
    assert "**Смотрите также:**" not in content


def test_format_class_skips_object_inheritance() -> None:
    block = DocBlock(
        entity_type="class",
        entity_name="Item",
        module_path="models.py",
        signature="class Item",
        summary="Item model.",
        inheritance="object",
    )
    content = format_markdown(block, "ru")
    assert "**Наследование:**" not in content
    assert "class Item" in content
    assert "(object)" not in content


def test_is_empty_section() -> None:
    assert is_empty_section("N/A")
    assert is_empty_section("n/a")
    assert is_empty_section("N/A\nextra explanation")
    assert is_empty_section("  **N/A**  ")
    assert is_empty_section("Нет побочных эффектов")
    assert is_empty_section("No side effects")
    assert not is_empty_section("ValueError on invalid input")
