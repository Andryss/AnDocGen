from __future__ import annotations

from andocgen.generator.base import OutputFormatter
from andocgen.models.entities import DocBlock


def render_doc_block(block: DocBlock, formatter: OutputFormatter, language: str) -> DocBlock:
    block.content = formatter.format(block, language)
    return block
