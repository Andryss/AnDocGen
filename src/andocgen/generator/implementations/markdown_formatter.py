from __future__ import annotations

from andocgen.generator.formatter import format_markdown
from andocgen.models.entities import DocBlock


class MarkdownOutputFormatter:
    def format(self, block: DocBlock, language: str = "ru") -> str:
        return format_markdown(block, language)
