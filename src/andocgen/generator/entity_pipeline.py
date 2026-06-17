from __future__ import annotations

import time
from typing import TYPE_CHECKING

from andocgen.config import ValidationConfig
from andocgen.generator.block_enricher import BlockEnricher
from andocgen.generator.entity_validator import (
    BlockingIssue,
    format_blocking_retry_prompt,
    validate_entity,
)
from andocgen.generator.implementations.markdown_section_parser import SectionParseError
from andocgen.generator.response_sanitizer import normalize_llm_response
from andocgen.llm.base import LLMProvider
from andocgen.models.entities import DocBlock, EntityContext, GenerationError

if TYPE_CHECKING:
    from andocgen.generator.base import OutputFormatter, SectionParser
    from andocgen.reporting.base import TraceLogger


class EntityDocumentPipeline:
    def __init__(
        self,
        section_parser: SectionParser,
        output_formatter: OutputFormatter,
        block_enricher: BlockEnricher | None = None,
    ) -> None:
        self._section_parser = section_parser
        self._output_formatter = output_formatter
        self._enricher = block_enricher or BlockEnricher()

    def run(
        self,
        ctx: EntityContext,
        llm: LLMProvider,
        system: str,
        user: str,
        language: str,
        max_retries: int,
        validation_config: ValidationConfig,
        trace: TraceLogger | None = None,
    ) -> tuple[DocBlock | None, GenerationError | None, float]:
        last_error = ""
        raw = ""
        start = time.perf_counter()
        blocking_issues: list[BlockingIssue] = []

        for attempt in range(max_retries + 1):
            attempt_user = user
            if attempt > 0:
                if blocking_issues:
                    attempt_user = (
                        f"{user}\n\n## Retry\n\n"
                        f"{format_blocking_retry_prompt(blocking_issues)}"
                    )
                elif last_error:
                    attempt_user = (
                        f"{user}\n\n## Retry\n\n"
                        f"Previous response failed parsing: {last_error}\n"
                        "Return ONLY the required ## sections in the exact format. "
                        "No JSON, no code fences."
                    )

            if trace:
                trace.log_llm_request(ctx.entity_id, system, attempt_user)

            try:
                raw = llm.complete(system, attempt_user)
                raw = normalize_llm_response(raw)
                block = self._section_parser.parse(raw, ctx)
                self._enricher.enrich(block, ctx)
                blocking_issues = validate_entity(block, ctx)

                if (
                    blocking_issues
                    and validation_config.retry_on_blocking
                    and attempt < max_retries
                ):
                    if trace:
                        trace.info(
                            f"  blocking validation for {ctx.entity_id}: "
                            + "; ".join(i.message for i in blocking_issues)
                        )
                    continue

                if blocking_issues and validation_config.blocking_fallback == "error":
                    duration_ms = (time.perf_counter() - start) * 1000
                    if trace:
                        trace.log_llm_response(ctx.entity_id, raw, duration_ms, parsed=False)
                    return None, GenerationError(
                        module_path=ctx.module_path,
                        entity_type=ctx.entity_type,
                        entity_name=ctx.entity_name,
                        message=blocking_issues[0].message,
                    ), duration_ms

                if blocking_issues and validation_config.blocking_fallback == "strip_examples":
                    block.examples = "N/A"

                block.content = self._output_formatter.format(block, language)
                duration_ms = (time.perf_counter() - start) * 1000
                if trace:
                    trace.log_llm_response(ctx.entity_id, raw, duration_ms, parsed=True)
                return block, None, duration_ms
            except SectionParseError as exc:
                last_error = str(exc)
                blocking_issues = []
                if trace and attempt == max_retries:
                    duration_ms = (time.perf_counter() - start) * 1000
                    trace.log_llm_response(ctx.entity_id, raw, duration_ms, parsed=False)

        duration_ms = (time.perf_counter() - start) * 1000
        message = last_error or (
            blocking_issues[0].message if blocking_issues else "Generation failed"
        )
        return None, GenerationError(
            module_path=ctx.module_path,
            entity_type=ctx.entity_type,
            entity_name=ctx.entity_name,
            message=message,
        ), duration_ms
