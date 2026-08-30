from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from andocgen.config import GenerationConfig, OutputConfig
from andocgen.generator.base import DocumentGenerator, OutputFormatter, SectionParser
from andocgen.generator.implementations.llm_generator import LlmDocumentGenerator
from andocgen.generator.implementations.markdown_formatter import MarkdownOutputFormatter
from andocgen.generator.implementations.markdown_section_parser import MarkdownSectionParser
from andocgen.registry import create_registered

_GENERATORS: dict[str, Callable[[SectionParser, OutputFormatter], DocumentGenerator]] = {
    "llm": LlmDocumentGenerator,
}

_SECTION_PARSERS: dict[str, type[SectionParser]] = {
    "markdown": MarkdownSectionParser,
}

_FORMATTERS: dict[str, type[OutputFormatter]] = {
    "markdown": MarkdownOutputFormatter,
}


@dataclass
class GeneratorComponents:
    document_generator: DocumentGenerator
    section_parser: SectionParser
    output_formatter: OutputFormatter


def create_generator_components(
    generation_config: GenerationConfig,
    output_config: OutputConfig,
) -> GeneratorComponents:
    section_parser = create_registered(_SECTION_PARSERS, output_config.implementation, "section parser")
    output_formatter = create_registered(_FORMATTERS, output_config.implementation, "output formatter")
    generator_cls = _GENERATORS.get(str(generation_config.implementation or "").lower())
    if generator_cls is None:
        raise ValueError(f"Unknown document generator implementation: {generation_config.implementation}")
    document_generator = generator_cls(section_parser, output_formatter)

    return GeneratorComponents(
        document_generator=document_generator,
        section_parser=section_parser,
        output_formatter=output_formatter,
    )
