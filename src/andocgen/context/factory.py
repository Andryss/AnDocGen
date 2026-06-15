from __future__ import annotations

from dataclasses import dataclass

from andocgen.config import ContextConfig
from andocgen.context.base import ContextBuilder, ProjectMetadataLoader, PromptBuilder
from andocgen.context.implementations.default_context import DefaultContextBuilder
from andocgen.context.implementations.metadata import DefaultProjectMetadataLoader
from andocgen.context.implementations.sectioned_prompt import SectionedPromptBuilder

_CONTEXT_BUILDERS: dict[str, type] = {
    "default": DefaultContextBuilder,
}

_PROMPT_BUILDERS: dict[str, type] = {
    "sectioned": SectionedPromptBuilder,
}

_METADATA_LOADERS: dict[str, type] = {
    "default": DefaultProjectMetadataLoader,
}


@dataclass
class ContextComponents:
    context_builder: ContextBuilder
    prompt_builder: PromptBuilder
    metadata_loader: ProjectMetadataLoader


def create_context_components(config: ContextConfig) -> ContextComponents:
    ctx_impl = config.implementation.lower()
    prompt_impl = config.prompt.lower()

    if ctx_impl not in _CONTEXT_BUILDERS:
        raise ValueError(f"Unknown context builder implementation: {config.implementation}")
    if prompt_impl not in _PROMPT_BUILDERS:
        raise ValueError(f"Unknown prompt builder implementation: {config.prompt}")

    return ContextComponents(
        context_builder=_CONTEXT_BUILDERS[ctx_impl](),
        prompt_builder=_PROMPT_BUILDERS[prompt_impl](),
        metadata_loader=_METADATA_LOADERS["default"](),
    )
