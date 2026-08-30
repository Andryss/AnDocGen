from __future__ import annotations

import json

from pydantic import ValidationError

from andocgen.llm.contracts import doc_response_to_block, response_model_for
from andocgen.models.entities import DocBlock, EntityContext
from andocgen.text.sections import is_empty_section


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

    try:
        response = response_model_for(ctx.entity_type).model_validate(payload)
    except ValidationError as exc:
        raise SectionParseError(_format_validation_error(exc)) from exc

    if not response.summary.strip():
        raise SectionParseError("JSON field `summary` must be a non-empty string")

    block = doc_response_to_block(response, ctx)
    block.raw_response = raw_response.strip()
    _normalize_empty_sections(block)
    return block


def _format_validation_error(exc: ValidationError) -> str:
    extra_fields = [
        ".".join(str(part) for part in error["loc"])
        for error in exc.errors()
        if error.get("type") == "extra_forbidden" and error.get("loc")
    ]
    if extra_fields:
        return f"Unexpected JSON fields: {', '.join(sorted(extra_fields))}"

    details = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"])
        details.append(location or str(error["type"]))
    if details:
        return f"JSON response failed contract validation: {', '.join(details)}"
    return "JSON response failed contract validation"


def _normalize_empty_sections(block: DocBlock) -> None:
    if block.raises is not None:
        block.raises = _normalize_optional_section(block.raises)
    if block.edge_cases is not None:
        block.edge_cases = _normalize_optional_section(block.edge_cases)
    if block.side_effects is not None:
        block.side_effects = _normalize_optional_section(block.side_effects)
    if block.see_also is not None:
        block.see_also = _normalize_optional_section(block.see_also)
    if block.purpose is not None:
        block.purpose = _normalize_optional_section(block.purpose)
    if block.usage_notes is not None:
        block.usage_notes = _normalize_optional_section(block.usage_notes)


def _normalize_optional_section(section: str) -> str:
    text = section.strip()
    if is_empty_section(text):
        return "N/A"
    return text
