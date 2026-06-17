from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from andocgen.config import ContextConfig, GenerationConfig, ValidationConfig
from andocgen.context.base import ContextBuilder, PromptBuilder
from andocgen.call_graph.base import CallGraphBuilder
from andocgen.llm.base import LLMProvider
from andocgen.models.entities import (
    CallGraph,
    DocBlock,
    EntityContext,
    GenerationError,
)
from andocgen.reporting.base import TraceLogger
from andocgen.reporting.progress import ProgressReporter


class DocumentGenerator(Protocol):
    def generate(
        self,
        ordered_contexts: list[EntityContext],
        llm: LLMProvider,
        generation_config: GenerationConfig,
        context_config: ContextConfig,
        call_graph: CallGraph,
        call_graph_builder: CallGraphBuilder,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        docs_by_id: dict[str, DocBlock] | None = None,
        trace: TraceLogger | None = None,
        progress: ProgressReporter | None = None,
        llm_factory: Callable[[], LLMProvider] | None = None,
        validation_config: ValidationConfig | None = None,
    ) -> tuple[list[DocBlock], list[GenerationError]]:
        ...


class SectionParser(Protocol):
    def parse(self, raw_response: str, ctx: EntityContext) -> DocBlock:
        ...


class OutputFormatter(Protocol):
    def format(self, block: DocBlock, language: str = "ru") -> str:
        ...
