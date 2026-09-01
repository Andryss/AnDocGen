from __future__ import annotations

from andocgen.llm.contracts import (
    ClassDocResponse,
    FunctionDocResponse,
    ModuleDocResponse,
    doc_response_schema,
)
from andocgen.llm.schema import docblock_schema


def test_doc_response_schema_is_generated_from_contract_models() -> None:
    assert doc_response_schema("function")["required"] == FunctionDocResponse.model_json_schema()["required"]
    assert doc_response_schema("method")["required"] == FunctionDocResponse.model_json_schema()["required"]
    assert doc_response_schema("class")["required"] == ClassDocResponse.model_json_schema()["required"]
    assert doc_response_schema("module")["required"] == ModuleDocResponse.model_json_schema()["required"]


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


def test_function_parameter_schema_requires_all_declared_properties() -> None:
    schema = docblock_schema("function")
    parameter = schema["properties"]["parameters"]["items"]

    assert set(parameter["properties"]) == {"name", "type", "description", "optional", "default"}
    assert parameter["required"] == ["name", "type", "description", "optional", "default"]
    assert parameter["additionalProperties"] is False


def test_provider_schema_omits_pydantic_metadata() -> None:
    schema = doc_response_schema("function")

    assert "title" not in schema
    assert '"default":' not in str(schema)


def test_module_schema_uses_export_objects() -> None:
    schema = docblock_schema("module")
    exports = schema["properties"]["exports"]

    assert exports["type"] == "array"
    assert exports["items"]["required"] == ["name", "type", "description"]
