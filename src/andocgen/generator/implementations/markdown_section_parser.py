from __future__ import annotations

from andocgen.generator.section_parser import SectionParseError, parse_sections
from andocgen.models.entities import DocBlock, EntityContext


class MarkdownSectionParser:
    def parse(self, raw_response: str, ctx: EntityContext) -> DocBlock:
        return parse_sections(raw_response, ctx)


__all__ = ["MarkdownSectionParser", "SectionParseError"]
