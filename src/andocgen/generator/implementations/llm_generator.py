from __future__ import annotations

import time

from andocgen.call_graph.base import CallGraphBuilder
from andocgen.config import ContextConfig, GenerationConfig
from andocgen.context.base import ContextBuilder, PromptBuilder
from andocgen.generator.base import OutputFormatter, SectionParser
from andocgen.generator.implementations.markdown_section_parser import SectionParseError
from andocgen.llm.base import LLMProvider
from andocgen.models.entities import (
    CallGraph,
    DocBlock,
    EntityContext,
    GenerationError,
)
from andocgen.reporting.base import TraceLogger


class LlmDocumentGenerator:
    def __init__(
        self,
        section_parser: SectionParser,
        output_formatter: OutputFormatter,
    ) -> None:
        self._section_parser = section_parser
        self._output_formatter = output_formatter

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
    ) -> tuple[list[DocBlock], list[GenerationError]]:
        blocks: list[DocBlock] = []
        errors: list[GenerationError] = []
        docs_by_id = docs_by_id or {}
        content_by_id: dict[str, str] = {k: v.content for k, v in docs_by_id.items()}

        for ctx in ordered_contexts:
            entity_label = f"{ctx.entity_type}:{ctx.entity_name}"
            if trace:
                trace.info(f"Generating {entity_label} ({ctx.entity_id})")

            callee_ids = (
                call_graph_builder.get_callee_ids(ctx.entity_id, call_graph)
                if context_config.include_call_graph
                else []
            )
            unresolved = (
                call_graph_builder.get_unresolved_calls(ctx.entity_id, call_graph)
                if context_config.include_call_graph
                else []
            )
            context_builder.attach_callee_docs(ctx, content_by_id, callee_ids, unresolved)

            if trace and unresolved:
                trace.debug(f"  unresolved calls for {ctx.entity_id}: {', '.join(unresolved)}")
            if trace and callee_ids:
                trace.debug(f"  callee docs attached: {len(callee_ids)}")

            system = prompt_builder.build_system_message(generation_config.language, ctx.entity_type)
            user = prompt_builder.build_user_message(ctx, context_config.max_context_chars)

            if trace:
                trace.log_llm_request(ctx.entity_id, system, user)

            start = time.perf_counter()
            raw = ""
            try:
                raw = llm.complete(system, user)
                duration_ms = (time.perf_counter() - start) * 1000
                block = self._section_parser.parse(raw, ctx)
                block.content = self._output_formatter.format(block, generation_config.language)
                blocks.append(block)
                content_by_id[ctx.entity_id] = block.content
                if trace:
                    trace.log_llm_response(ctx.entity_id, raw, duration_ms, parsed=True)
                    param_count = len(block.parameters or [])
                    trace.debug(
                        f"  parsed {entity_label}: params={param_count} "
                        f"summary_len={len(block.summary)}"
                    )
            except SectionParseError as exc:
                duration_ms = (time.perf_counter() - start) * 1000
                if trace:
                    trace.log_llm_response(ctx.entity_id, raw, duration_ms, parsed=False)
                    trace.error(f"  section parse failed for {entity_label}: {exc}")
                errors.append(
                    GenerationError(
                        module_path=ctx.module_path,
                        entity_type=ctx.entity_type,
                        entity_name=ctx.entity_name,
                        message=str(exc),
                    )
                )

        return blocks, errors
