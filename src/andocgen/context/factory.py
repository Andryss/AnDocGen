from __future__ import annotations

from dataclasses import dataclass

from andocgen.config import ContextConfig
from andocgen.context.base import ContextBuilder, ProjectMetadataLoader, PromptBuilder
from andocgen.context.implementations.default_context import DefaultContextBuilder
from andocgen.context.implementations.metadata import DefaultProjectMetadataLoader
from andocgen.context.implementations.sectioned_prompt import SectionedPromptBuilder
from andocgen.registry import create_registered

_CONTEXT_BUILDERS: dict[str, type[ContextBuilder]] = {
    "default": DefaultContextBuilder,
}

_PROMPT_BUILDERS: dict[str, type[PromptBuilder]] = {
    "sectioned": SectionedPromptBuilder,
}

_METADATA_LOADERS: dict[str, type[ProjectMetadataLoader]] = {
    "default": DefaultProjectMetadataLoader,
}


@dataclass
class ContextComponents:
    context_builder: ContextBuilder
    prompt_builder: PromptBuilder
    metadata_loader: ProjectMetadataLoader


def create_context_components(config: ContextConfig) -> ContextComponents:
    return ContextComponents(
        context_builder=create_registered(_CONTEXT_BUILDERS, config.implementation, "context builder"),
        prompt_builder=create_registered(_PROMPT_BUILDERS, config.prompt, "prompt builder"),
        metadata_loader=_METADATA_LOADERS["default"](),
    )
