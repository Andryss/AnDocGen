from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from andocgen.models.entities import (
    DocBlock,
    EntityContext,
    EntityType,
    ExampleDoc,
    ExportDoc,
    ParameterDoc,
    ReturnDoc,
)


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ParameterResponse(_StrictModel):
    name: str
    type: str
    description: str
    optional: bool
    default: str | None


class ReturnResponse(_StrictModel):
    type: str
    description: str


class ExampleResponse(_StrictModel):
    description: str
    language: str
    code: str


class ExportResponse(_StrictModel):
    name: str
    type: str
    description: str


class FunctionDocResponse(_StrictModel):
    summary: str
    parameters: list[ParameterResponse]
    returns: ReturnResponse | None
    raises: str
    edge_cases: str
    side_effects: str
    examples: list[ExampleResponse]
    see_also: str


class ClassDocResponse(_StrictModel):
    summary: str
    purpose: str
    usage_notes: str


class ModuleDocResponse(_StrictModel):
    summary: str
    exports: list[ExportResponse]


DocResponse = FunctionDocResponse | ClassDocResponse | ModuleDocResponse


def doc_response_schema(
    entity_type: EntityType | Literal["function", "method", "class", "module"],
) -> dict[str, Any]:
    schema = _response_model(entity_type).model_json_schema()
    return _strip_schema_metadata(_inline_refs(schema))


def response_model_for(
    entity_type: EntityType | Literal["function", "method", "class", "module"],
) -> type[FunctionDocResponse] | type[ClassDocResponse] | type[ModuleDocResponse]:
    return _response_model(entity_type)


def doc_response_to_block(response: DocResponse, ctx: EntityContext) -> DocBlock:
    block = DocBlock(
        entity_type=ctx.entity_type,
        entity_name=ctx.entity_name,
        module_path=ctx.module_path,
        signature=ctx.signature,
        summary=response.summary.strip(),
    )
    if isinstance(response, FunctionDocResponse):
        block.parameters = [
            ParameterDoc(
                name=param.name.strip(),
                type=param.type.strip(),
                description=param.description.strip(),
                optional=param.optional,
                default=param.default,
            )
            for param in _dedupe_by_name(response.parameters)
        ]
        block.returns = (
            ReturnDoc(type=response.returns.type.strip(), description=response.returns.description.strip())
            if response.returns
            else None
        )
        block.raises = response.raises.strip()
        block.edge_cases = response.edge_cases.strip()
        block.side_effects = response.side_effects.strip()
        block.examples = [
            ExampleDoc(
                description=example.description.strip(),
                language=example.language.strip(),
                code=example.code.strip(),
            )
            for example in response.examples
        ]
        block.see_also = response.see_also.strip()
    elif isinstance(response, ClassDocResponse):
        block.purpose = response.purpose.strip()
        block.usage_notes = response.usage_notes.strip()
    else:
        block.exports = [
            ExportDoc(
                name=export.name.strip(),
                type=export.type.strip(),
                description=export.description.strip(),
            )
            for export in response.exports
        ]
    return block


def _response_model(entity_type: str) -> type[FunctionDocResponse] | type[ClassDocResponse] | type[ModuleDocResponse]:
    if entity_type in ("function", "method"):
        return FunctionDocResponse
    if entity_type == "class":
        return ClassDocResponse
    return ModuleDocResponse


def _dedupe_by_name(parameters: list[ParameterResponse]) -> list[ParameterResponse]:
    seen: set[str] = set()
    result: list[ParameterResponse] = []
    for param in parameters:
        name = param.name.strip()
        if name in seen:
            continue
        seen.add(name)
        result.append(param)
    return result


def _inline_refs(schema: dict[str, Any]) -> dict[str, Any]:
    defs = schema.pop("$defs", {})

    def resolve(value: Any) -> Any:
        if isinstance(value, dict):
            ref = value.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/$defs/"):
                target = defs.get(ref.rsplit("/", 1)[-1], {})
                return resolve(dict(target))
            return {key: resolve(item) for key, item in value.items()}
        if isinstance(value, list):
            return [resolve(item) for item in value]
        return value

    return resolve(schema)


def _strip_schema_metadata(schema: dict[str, Any]) -> dict[str, Any]:
    def strip(value: Any) -> Any:
        if isinstance(value, dict):
            result: dict[str, Any] = {}
            for key, item in value.items():
                if key == "properties" and isinstance(item, dict):
                    result[key] = {name: strip(prop_schema) for name, prop_schema in item.items()}
                    continue
                if key in {"title", "default"}:
                    continue
                result[key] = strip(item)
            return result
        if isinstance(value, list):
            return [strip(item) for item in value]
        return value

    return strip(schema)
