from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DocBriefRegistry:
    summary_by_id: dict[str, str] = field(default_factory=dict)
    signature_by_id: dict[str, str] = field(default_factory=dict)
    entity_type_by_id: dict[str, str] = field(default_factory=dict)

    def register(self, entity_id: str, summary: str, signature: str, entity_type: str) -> None:
        self.summary_by_id[entity_id] = summary.strip()
        if signature:
            self.signature_by_id[entity_id] = signature.strip()
        self.entity_type_by_id[entity_id] = entity_type

    def brief_line(self, entity_id: str, fallback_signature: str = "") -> str:
        signature = self.signature_by_id.get(entity_id) or fallback_signature or entity_id
        summary = self.summary_by_id.get(entity_id, "(not documented)")
        return f"- `{signature}` — {summary}"

    def has(self, entity_id: str) -> bool:
        return entity_id in self.summary_by_id
