from __future__ import annotations

from typing import Any


def docblock_schema(entity_type: str = "function") -> dict[str, Any]:
    parameter = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "type": {"type": "string"},
            "description": {"type": "string"},
        },
        "required": ["name", "type", "description"],
        "additionalProperties": False,
    }
    example = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "language": {"type": "string"},
            "code": {"type": "string"},
        },
        "required": ["description", "language", "code"],
        "additionalProperties": False,
    }
    if entity_type == "class":
        text_field = {"type": "string"}
        return {
            "type": "object",
            "properties": {
                "summary": text_field,
                "purpose": text_field,
                "usage_notes": text_field,
            },
            "required": ["summary", "purpose", "usage_notes"],
            "additionalProperties": False,
        }
    if entity_type == "module":
        return {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "exports": {"type": "array", "items": parameter},
            },
            "required": ["summary", "exports"],
            "additionalProperties": False,
        }
    text_field = {"type": "string"}
    return {
        "type": "object",
        "properties": {
            "summary": text_field,
            "parameters": {"type": "array", "items": parameter},
            "returns": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["type", "description"],
                        "additionalProperties": False,
                    },
                    {"type": "null"},
                ]
            },
            "raises": text_field,
            "edge_cases": text_field,
            "side_effects": text_field,
            "examples": {"type": "array", "items": example},
            "see_also": text_field,
        },
        "required": [
            "summary",
            "parameters",
            "returns",
            "raises",
            "edge_cases",
            "side_effects",
            "examples",
            "see_also",
        ],
        "additionalProperties": False,
    }
