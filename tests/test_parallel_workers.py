from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor

from andocgen.config import ContextConfig, GenerationConfig, ValidationConfig
from andocgen.generator.implementations.llm_generator import LlmDocumentGenerator
from andocgen.generator.implementations.markdown_formatter import MarkdownOutputFormatter
from andocgen.generator.implementations.markdown_section_parser import MarkdownSectionParser
from andocgen.models.entities import CallGraph, EntityContext


class _SlowLLM:
    _global_concurrent = 0
    _global_max = 0
    _global_lock = threading.Lock()

    def __init__(self, delay: float = 0.05) -> None:
        self.delay = delay

    def complete(self, system: str, user: str) -> str:
        with _SlowLLM._global_lock:
            _SlowLLM._global_concurrent += 1
            _SlowLLM._global_max = max(_SlowLLM._global_max, _SlowLLM._global_concurrent)
        try:
            time.sleep(self.delay)
            return """## Summary

Ok.

## Parameters

N/A

## Returns

N/A

## Raises

N/A

## Edge cases

N/A

## Side effects

N/A

## Examples

N/A

## See also

N/A
"""
        finally:
            with _SlowLLM._global_lock:
                _SlowLLM._global_concurrent -= 1


class _SlowLLMFactory:
    def __init__(self, delay: float = 0.05) -> None:
        self.delay = delay
        _SlowLLM._global_max = 0

    def __call__(self) -> _SlowLLM:
        return _SlowLLM(self.delay)


class _NoOpContextBuilder:
    def attach_callee_docs(self, ctx, docs_by_id, callee_ids, unresolved) -> None:
        pass

    def attach_related_briefs(
        self, ctx, registry, callee_ids, unresolved, call_graph=None
    ) -> None:
        pass


class _NoOpPromptBuilder:
    def build_system_message(self, language: str, entity_type: str) -> str:
        return "system"

    def build_user_message(self, ctx: EntityContext, max_chars: int) -> str:
        return "user"


class _NoOpCallGraphBuilder:
    def get_callee_ids(self, entity_id: str, graph: CallGraph) -> list[str]:
        return []

    def get_unresolved_calls(self, entity_id: str, graph: CallGraph) -> list[str]:
        return []


def _function_ctx(name: str) -> EntityContext:
    return EntityContext(
        entity_type="function",
        entity_name=name,
        entity_id=f"m.py::{name}",
        module_path="m.py",
        project_name="demo",
        signature=f"def {name}()",
    )


def test_parallel_workers_use_thread_pool() -> None:
    contexts = [_function_ctx(f"fn{i}") for i in range(8)]
    gen = LlmDocumentGenerator(MarkdownSectionParser(), MarkdownOutputFormatter())
    factory = _SlowLLMFactory(delay=0.05)
    config = GenerationConfig(workers=4, max_retries=0)

    start = time.perf_counter()
    blocks, errors = gen.generate(
        contexts,
        _SlowLLM(),
        config,
        ContextConfig(include_call_graph=False),
        CallGraph(),
        _NoOpCallGraphBuilder(),
        _NoOpContextBuilder(),
        _NoOpPromptBuilder(),
        llm_factory=factory,
        validation_config=ValidationConfig(),
    )
    elapsed = time.perf_counter() - start

    assert not errors
    assert len(blocks) == 8
    assert _SlowLLM._global_max >= 2
    assert elapsed < 8 * 0.05 * 0.9
