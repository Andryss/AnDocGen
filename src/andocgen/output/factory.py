from __future__ import annotations

from dataclasses import dataclass

from andocgen.config import OutputConfig
from andocgen.output.base import CacheStore, DocumentationWriter, PreviousDocLoader
from andocgen.output.implementations.json_cache import JsonCacheStore
from andocgen.output.implementations.markdown_previous_doc import MarkdownPreviousDocLoader
from andocgen.output.implementations.markdown_writer import MarkdownDocumentationWriter
from andocgen.registry import create_registered

_WRITERS: dict[str, type[DocumentationWriter]] = {
    "markdown": MarkdownDocumentationWriter,
}

_CACHE_STORES: dict[str, type[CacheStore]] = {
    "json": JsonCacheStore,
}

_PREVIOUS_DOC_LOADERS: dict[str, type[PreviousDocLoader]] = {
    "markdown": MarkdownPreviousDocLoader,
}


@dataclass
class OutputComponents:
    writer: DocumentationWriter
    cache_store: CacheStore
    previous_doc_loader: PreviousDocLoader


def create_output_components(config: OutputConfig) -> OutputComponents:
    return OutputComponents(
        writer=create_registered(_WRITERS, config.implementation, "output writer"),
        cache_store=_CACHE_STORES["json"](),
        previous_doc_loader=create_registered(
            _PREVIOUS_DOC_LOADERS,
            config.implementation,
            "previous document loader",
        ),
    )
