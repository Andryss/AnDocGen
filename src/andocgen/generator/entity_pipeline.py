from __future__ import annotations

import time
from typing import TYPE_CHECKING

from andocgen.config import ValidationConfig
from andocgen.generator.block_enricher import BlockEnricher
from andocgen.generator.entity_validator import (
    BlockingIssue,
    format_blocking_retry_prompt,
    validate_entity,
    validate_summary_language,
)
from andocgen.generator.fallback import build_fallback_block
from andocgen.generator.implementations.markdown_section_parser import SectionParseError
from andocgen.generator.rendering import render_doc_block
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
            retry_reason = None
            if attempt > 0:
                if blocking_issues:
                    retry_reason = "; ".join(issue.message for issue in blocking_issues)
                    attempt_user = (
                        f"{user}\n\n## Retry\n\n"
                        f"{format_blocking_retry_prompt(blocking_issues)}"
                    )
                elif last_error:
                    retry_reason = last_error
                    if ctx.entity_type == "class":
                        lang = "Russian" if language == "ru" else language
                        attempt_user = (
                            f"{user}\n\n## Retry\n\n"
                            f"Previous response failed parsing: {last_error}\n"
                            f"Return ONLY a valid JSON object with the `summary` string in {lang}. No code fences."
                        )
                    else:
                        attempt_user = (
                            f"{user}\n\n## Retry\n\n"
                            f"Previous response failed parsing: {last_error}\n"
                            "Return ONLY the required JSON object. No Markdown and no code fences."
                        )

            if trace:
                trace.log_llm_request(ctx.entity_id, system, attempt_user)

            try:
                raw = llm.complete(system, attempt_user, entity_type=ctx.entity_type)
                raw = normalize_llm_response(raw)
                block = self._section_parser.parse(raw, ctx)
                self._enricher.enrich(block, ctx)
                blocking_issues = validate_entity(block, ctx)
                blocking_issues.extend(validate_summary_language(block, ctx))

                if (
                    blocking_issues
                    and validation_config.retry_on_blocking
                    and attempt < max_retries
                ):
                    duration_ms = (time.perf_counter() - start) * 1000
                    if trace:
                        trace.log_llm_attempt(
                            entity_id=ctx.entity_id,
                            entity_type=ctx.entity_type,
                            entity_name=ctx.entity_name,
                            module_path=ctx.module_path,
                            provider=type(llm).__name__,
                            model=str(getattr(llm, "model", "mock")),
                            attempt=attempt,
                            duration_ms=duration_ms,
                            system=system,
                            user=attempt_user,
                            raw_response=raw,
                            parse_ok=True,
                            validation_ok=False,
                            retry_reason="; ".join(i.message for i in blocking_issues),
                            structured_format="json_schema",
                        )
                        trace.info(
                            f"  blocking validation for {ctx.entity_id}: "
                            + "; ".join(i.message for i in blocking_issues)
                        )
                    continue

                if blocking_issues and validation_config.blocking_fallback == "error":
                    duration_ms = (time.perf_counter() - start) * 1000
                    if trace:
                        trace.log_llm_response(ctx.entity_id, raw, duration_ms, parsed=False)
                        trace.log_llm_attempt(
                            entity_id=ctx.entity_id,
                            entity_type=ctx.entity_type,
                            entity_name=ctx.entity_name,
                            module_path=ctx.module_path,
                            provider=type(llm).__name__,
                            model=str(getattr(llm, "model", "mock")),
                            attempt=attempt,
                            duration_ms=duration_ms,
                            system=system,
                            user=attempt_user,
                            raw_response=raw,
                            parse_ok=True,
                            validation_ok=False,
                            fallback_reason=blocking_issues[0].message,
                            structured_format="json_schema",
                        )
                    return None, GenerationError(
                        module_path=ctx.module_path,
                        entity_type=ctx.entity_type,
                        entity_name=ctx.entity_name,
                        message=blocking_issues[0].message,
                    ), duration_ms

                if blocking_issues and validation_config.blocking_fallback == "strip_examples":
                    block.examples = []

                render_doc_block(block, self._output_formatter, language)
                duration_ms = (time.perf_counter() - start) * 1000
                if trace:
                    trace.log_llm_response(ctx.entity_id, raw, duration_ms, parsed=True)
                    trace.log_llm_attempt(
                        entity_id=ctx.entity_id,
                        entity_type=ctx.entity_type,
                        entity_name=ctx.entity_name,
                        module_path=ctx.module_path,
                        provider=type(llm).__name__,
                        model=str(getattr(llm, "model", "mock")),
                        attempt=attempt,
                        duration_ms=duration_ms,
                        system=system,
                        user=attempt_user,
                        raw_response=raw,
                        parse_ok=True,
                        validation_ok=not blocking_issues,
                        structured_format="json_schema",
                    )
                return block, None, duration_ms
            except SectionParseError as exc:
                last_error = str(exc)
                blocking_issues = []
                if trace:
                    duration_ms = (time.perf_counter() - start) * 1000
                    if attempt == max_retries:
                        trace.log_llm_response(ctx.entity_id, raw, duration_ms, parsed=False)
                    trace.log_llm_attempt(
                        entity_id=ctx.entity_id,
                        entity_type=ctx.entity_type,
                        entity_name=ctx.entity_name,
                        module_path=ctx.module_path,
                        provider=type(llm).__name__,
                        model=str(getattr(llm, "model", "mock")),
                        attempt=attempt,
                        duration_ms=duration_ms,
                        system=system,
                        user=attempt_user,
                        raw_response=raw,
                        parse_ok=False,
                        validation_ok=False,
                        retry_reason=retry_reason,
                        fallback_reason=last_error if attempt == max_retries else None,
                        structured_format="json_schema",
                    )
            except Exception as exc:
                last_error = str(exc)
                blocking_issues = []
                if trace:
                    duration_ms = (time.perf_counter() - start) * 1000
                    trace.log_llm_attempt(
                        entity_id=ctx.entity_id,
                        entity_type=ctx.entity_type,
                        entity_name=ctx.entity_name,
                        module_path=ctx.module_path,
                        provider=type(llm).__name__,
                        model=str(getattr(llm, "model", "mock")),
                        attempt=attempt,
                        duration_ms=duration_ms,
                        system=system,
                        user=attempt_user,
                        raw_response=raw,
                        parse_ok=False,
                        validation_ok=False,
                        retry_reason=retry_reason,
                        fallback_reason=last_error if attempt == max_retries else None,
                        structured_format="json_schema",
                    )

        duration_ms = (time.perf_counter() - start) * 1000
        reason = last_error or "; ".join(issue.message for issue in blocking_issues) or "exhausted retries"
        block = build_fallback_block(ctx, raw, reason=reason)
        render_doc_block(block, self._output_formatter, language)
        if trace:
            trace.info(f"  fallback generated for {ctx.entity_id}")
        return block, None, duration_ms
