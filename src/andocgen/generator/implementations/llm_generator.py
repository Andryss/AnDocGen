from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from andocgen.call_graph.base import CallGraphBuilder
from andocgen.config import ContextConfig, GenerationConfig, ValidationConfig
from andocgen.context.base import ContextBuilder, PromptBuilder
from andocgen.generator.base import OutputFormatter, SectionParser
from andocgen.generator.entity_pipeline import EntityDocumentPipeline
from andocgen.generator.waves import group_into_waves
from andocgen.llm.base import LLMProvider
from andocgen.models.entities import (
    CallGraph,
    DocBlock,
    EntityContext,
    GenerationError,
)
from andocgen.reporting.base import TraceLogger
from andocgen.reporting.progress import ProgressReporter


class LlmDocumentGenerator:
    def __init__(
        self,
        section_parser: SectionParser,
        output_formatter: OutputFormatter,
    ) -> None:
        self._pipeline = EntityDocumentPipeline(section_parser, output_formatter)

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
        blocks: list[DocBlock] = []
        errors: list[GenerationError] = []
        docs_by_id = docs_by_id or {}
        content_by_id: dict[str, str] = {k: v.content for k, v in docs_by_id.items()}
        validation = validation_config or ValidationConfig()

        waves = group_into_waves(ordered_contexts, call_graph, call_graph_builder)
        total = len(ordered_contexts)
        workers = max(1, generation_config.workers)
        completed = 0
        progress_lock = threading.Lock()
        content_lock = threading.Lock()

        def bump_progress(entity_id: str, duration_ms: float, ok: bool) -> int:
            nonlocal completed
            with progress_lock:
                completed += 1
                current = completed
            if progress:
                progress.on_llm_progress(current, total, entity_id, duration_ms, ok)
            return current

        def run_one(ctx: EntityContext) -> tuple[DocBlock | None, GenerationError | None]:
            provider = llm_factory() if llm_factory else llm
            with content_lock:
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

            entity_label = f"{ctx.entity_type}:{ctx.entity_name}"
            if trace:
                trace.info(f"Generating {entity_label} ({ctx.entity_id})")

            system = prompt_builder.build_system_message(
                generation_config.language, ctx.entity_type
            )
            user = prompt_builder.build_user_message(ctx, context_config.max_context_chars)

            block, err, duration_ms = self._pipeline.run(
                ctx,
                provider,
                system,
                user,
                generation_config.language,
                generation_config.max_retries,
                validation,
                trace,
            )
            bump_progress(ctx.entity_id, duration_ms, block is not None)
            if err and trace:
                trace.error(f"  generation failed for {entity_label}: {err.message}")
            return block, err

        for wave in waves:
            wave_workers = 1 if len(wave) == 1 and wave[0].entity_type == "module" else workers
            if wave_workers == 1:
                for ctx in wave:
                    block, err = run_one(ctx)
                    if block:
                        blocks.append(block)
                        with content_lock:
                            content_by_id[ctx.entity_id] = block.content
                    if err:
                        errors.append(err)
            else:
                with ThreadPoolExecutor(max_workers=wave_workers) as pool:
                    futures = {pool.submit(run_one, ctx): ctx for ctx in wave}
                    for future in as_completed(futures):
                        ctx = futures[future]
                        block, err = future.result()
                        if block:
                            blocks.append(block)
                            with content_lock:
                                content_by_id[ctx.entity_id] = block.content
                        if err:
                            errors.append(err)

        return blocks, errors
