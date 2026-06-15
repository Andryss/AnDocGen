from __future__ import annotations

from dataclasses import dataclass

from andocgen.config import GenerationConfig, OutputConfig
from andocgen.generator.base import DocumentGenerator, OutputFormatter, SectionParser
from andocgen.generator.implementations.llm_generator import LlmDocumentGenerator
from andocgen.generator.implementations.markdown_formatter import MarkdownOutputFormatter
from andocgen.generator.implementations.markdown_section_parser import MarkdownSectionParser

_GENERATORS: dict[str, type] = {
    "llm": LlmDocumentGenerator,
}

_SECTION_PARSERS: dict[str, type] = {
    "markdown": MarkdownSectionParser,
}

_FORMATTERS: dict[str, type] = {
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
    gen_impl = generation_config.implementation.lower()
    fmt_impl = output_config.implementation.lower()

    if gen_impl not in _GENERATORS:
        raise ValueError(f"Unknown document generator implementation: {generation_config.implementation}")
    if fmt_impl not in _SECTION_PARSERS:
        raise ValueError(f"Unknown section parser implementation: {output_config.implementation}")
    if fmt_impl not in _FORMATTERS:
        raise ValueError(f"Unknown output formatter implementation: {output_config.implementation}")

    section_parser = _SECTION_PARSERS[fmt_impl]()
    output_formatter = _FORMATTERS[fmt_impl]()
    document_generator = _GENERATORS[gen_impl](section_parser, output_formatter)

    return GeneratorComponents(
        document_generator=document_generator,
        section_parser=section_parser,
        output_formatter=output_formatter,
    )
