from __future__ import annotations

from typing import Any

from andocgen.llm.contracts import doc_response_schema


def docblock_schema(entity_type: str = "function") -> dict[str, Any]:
    return doc_response_schema(entity_type)  # type: ignore[arg-type]
