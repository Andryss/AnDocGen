from __future__ import annotations

import json
from typing import Any

from andocgen.generator.formatter import is_empty_section
from andocgen.models.entities import (
    DocBlock,
    EntityContext,
    EntityType,
    ExportDoc,
    ParameterDoc,
    ReturnDoc,
)


class SectionParseError(Exception):
    pass


def parse_sections(raw_response: str, ctx: EntityContext) -> DocBlock:
    from andocgen.generator.response_sanitizer import normalize_llm_response

    raw_response = normalize_llm_response(raw_response)
    if _looks_like_json(raw_response):
        return _parse_json_response(raw_response, ctx)
    raise SectionParseError("Response must be a JSON object")


def _looks_like_json(text: str) -> bool:
    stripped = text.strip()
    return stripped.startswith("{") and stripped.endswith("}")


def _parse_json_response(raw_response: str, ctx: EntityContext) -> DocBlock:
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise SectionParseError(f"Malformed JSON response: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise SectionParseError("JSON response must be an object")

    allowed = _json_allowed_fields(ctx.entity_type)
    unexpected = sorted(set(payload) - allowed)
    if unexpected:
        raise SectionParseError(f"Unexpected JSON fields: {', '.join(unexpected)}")

    required = _json_required_fields(ctx.entity_type)
    missing = [field for field in required if field not in payload]
    if missing:
        raise SectionParseError(f"Missing JSON fields: {', '.join(missing)}")

    summary = payload.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise SectionParseError("JSON field `summary` must be a non-empty string")

    block = DocBlock(
        entity_type=ctx.entity_type,
        entity_name=ctx.entity_name,
        module_path=ctx.module_path,
        signature=ctx.signature,
        raw_response=raw_response.strip(),
        summary=summary.strip(),
    )

    if ctx.entity_type in ("function", "method"):
        block.parameters = _json_parameters(payload.get("parameters"))
        block.returns = _json_return(payload.get("returns"))
        block.raises = _json_optional_text(payload.get("raises"), "raises")
        block.edge_cases = _json_optional_text(payload.get("edge_cases"), "edge_cases")
        block.side_effects = _json_optional_text(payload.get("side_effects"), "side_effects")
        block.examples = _json_optional_text(payload.get("examples"), "examples")
        block.see_also = _json_optional_text(payload.get("see_also"), "see_also")
    elif ctx.entity_type == "class":
        block.fields = _json_parameters(payload.get("fields", []))
        block.inheritance = _json_optional_text(payload.get("inheritance", "N/A"), "inheritance")
        block.methods_overview = _json_optional_text(payload.get("methods_overview", "N/A"), "methods_overview")
    elif ctx.entity_type == "module":
        block.exports = _json_exports(payload.get("exports"))

    return block


def _json_allowed_fields(entity_type: EntityType) -> set[str]:
    if entity_type in ("function", "method"):
        return {
            "summary",
            "parameters",
            "returns",
            "raises",
            "edge_cases",
            "side_effects",
            "examples",
            "see_also",
        }
    if entity_type == "class":
        return {"summary", "fields", "inheritance", "methods_overview"}
    return {"summary", "exports"}


def _json_required_fields(entity_type: EntityType) -> list[str]:
    if entity_type in ("function", "method"):
        return [
            "summary",
            "parameters",
            "returns",
            "raises",
            "edge_cases",
            "side_effects",
            "examples",
            "see_also",
        ]
    if entity_type == "class":
        return ["summary"]
    return ["summary", "exports"]


def _json_parameters(value: Any) -> list[ParameterDoc]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise SectionParseError("JSON parameter list must be an array")
    params: list[ParameterDoc] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, dict):
            raise SectionParseError("JSON parameter item must be an object")
        extra = sorted(set(item) - {"name", "type", "description", "optional", "default"})
        if extra:
            raise SectionParseError(f"Unexpected JSON parameter fields: {', '.join(extra)}")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SectionParseError("JSON parameter `name` must be a non-empty string")
        if name in seen:
            continue
        typ = item.get("type", "")
        desc = item.get("description", "")
        default = item.get("default")
        params.append(
            ParameterDoc(
                name=name.strip(),
                type=typ.strip() if isinstance(typ, str) else "",
                description=desc.strip() if isinstance(desc, str) else "",
                optional=bool(item.get("optional", False)),
                default=default if isinstance(default, str) else None,
            )
        )
        seen.add(name)
    return params


def _json_return(value: Any) -> ReturnDoc | None:
    if value is None:
        return None
    if isinstance(value, str):
        if is_empty_section(value):
            return None
        return ReturnDoc(type="", description=value.strip())
    if not isinstance(value, dict):
        raise SectionParseError("JSON `returns` must be null, string, or object")
    extra = sorted(set(value) - {"type", "description"})
    if extra:
        raise SectionParseError(f"Unexpected JSON return fields: {', '.join(extra)}")
    typ = value.get("type", "")
    desc = value.get("description", "")
    if not typ and not desc:
        return None
    return ReturnDoc(
        type=typ.strip() if isinstance(typ, str) else "",
        description=desc.strip() if isinstance(desc, str) else "",
    )


def _json_exports(value: Any) -> list[ExportDoc]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise SectionParseError("JSON exports list must be an array")
    exports: list[ExportDoc] = []
    for item in value:
        if not isinstance(item, dict):
            raise SectionParseError("JSON export item must be an object")
        extra = sorted(set(item) - {"name", "type", "description"})
        if extra:
            raise SectionParseError(f"Unexpected JSON export fields: {', '.join(extra)}")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SectionParseError("JSON export `name` must be a non-empty string")
        typ = item.get("type")
        desc = item.get("description", "")
        exports.append(
            ExportDoc(
                name=name.strip(),
                type=typ.strip() if isinstance(typ, str) else None,
                description=desc.strip() if isinstance(desc, str) else "",
            )
        )
    return exports


def _json_optional_text(value: Any, field: str) -> str:
    if value is None:
        return "N/A"
    if not isinstance(value, str):
        raise SectionParseError(f"JSON field `{field}` must be a string")
    return _normalize_optional_section(value)


def _normalize_optional_section(section: str) -> str:
    text = section.strip()
    if is_empty_section(text):
        return "N/A"
    return text
