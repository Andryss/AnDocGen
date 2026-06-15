from __future__ import annotations

from dataclasses import dataclass

from andocgen.config import OutputConfig
from andocgen.output.base import CacheStore, DocumentationWriter, PreviousDocLoader
from andocgen.output.implementations.json_cache import JsonCacheStore
from andocgen.output.implementations.markdown_previous_doc import MarkdownPreviousDocLoader
from andocgen.output.implementations.markdown_writer import MarkdownDocumentationWriter

_WRITERS: dict[str, type] = {
    "markdown": MarkdownDocumentationWriter,
}

_CACHE_STORES: dict[str, type] = {
    "json": JsonCacheStore,
}

_PREVIOUS_DOC_LOADERS: dict[str, type] = {
    "markdown": MarkdownPreviousDocLoader,
}


@dataclass
class OutputComponents:
    writer: DocumentationWriter
    cache_store: CacheStore
    previous_doc_loader: PreviousDocLoader


def create_output_components(config: OutputConfig) -> OutputComponents:
    impl = config.implementation.lower()
    if impl not in _WRITERS:
        raise ValueError(f"Unknown output writer implementation: {config.implementation}")

    return OutputComponents(
        writer=_WRITERS[impl](),
        cache_store=_CACHE_STORES["json"](),
        previous_doc_loader=_PREVIOUS_DOC_LOADERS.get(impl, MarkdownPreviousDocLoader)(),
    )
