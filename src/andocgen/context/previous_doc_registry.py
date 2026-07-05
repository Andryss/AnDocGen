from __future__ import annotations

from andocgen.context.doc_brief_registry import DocBriefRegistry
from andocgen.models.entities import EntityContext


def summary_from_doc_fragment(doc_text: str) -> str:
    lines = [line.strip() for line in doc_text.strip().splitlines() if line.strip()]
    if not lines:
        return "(not documented)"
    if lines[0].startswith("### "):
        lines = lines[1:]
    for line in lines:
        if line.startswith("**") and line.endswith("**"):
            continue
        if line.startswith("|") or line.startswith("-") or line.startswith("```"):
            continue
        return line[:500]
    return lines[0][:500]


def seed_registry_from_previous_docs(
    registry: DocBriefRegistry,
    previous_docs: dict[str, str],
    contexts: list[EntityContext],
) -> None:
    context_by_id = {ctx.entity_id: ctx for ctx in contexts}
    for entity_id, doc_text in previous_docs.items():
        ctx = context_by_id.get(entity_id)
        registry.register(
            entity_id,
            summary_from_doc_fragment(doc_text),
            ctx.signature if ctx else "",
            ctx.entity_type if ctx else "function",
        )
