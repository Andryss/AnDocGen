from __future__ import annotations

from andocgen.llm.schema import docblock_schema


def test_class_schema_contains_semantic_fields() -> None:
    schema = docblock_schema("class")

    assert schema["required"] == ["summary", "purpose", "usage_notes"]
    assert set(schema["properties"]) == {"summary", "purpose", "usage_notes"}
    assert schema["additionalProperties"] is False


def test_function_schema_contains_typed_examples() -> None:
    schema = docblock_schema("function")
    example = schema["properties"]["examples"]["items"]

    assert example["required"] == ["description", "language", "code"]
    assert example["additionalProperties"] is False


def test_module_schema_uses_export_objects() -> None:
    schema = docblock_schema("module")
    exports = schema["properties"]["exports"]

    assert exports["type"] == "array"
    assert exports["items"]["required"] == ["name", "type", "description"]
