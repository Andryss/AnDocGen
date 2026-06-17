from __future__ import annotations

from andocgen.config import ValidationConfig
from andocgen.generator.entity_pipeline import EntityDocumentPipeline
from andocgen.generator.implementations.markdown_formatter import MarkdownOutputFormatter
from andocgen.generator.implementations.markdown_section_parser import MarkdownSectionParser
from andocgen.models.entities import (
    ClassModel,
    DocBlock,
    EntityContext,
    FunctionModel,
    ModuleModel,
    ParameterModel,
)


class _SequenceLLM:
    def __init__(self, responses: list[str]) -> None:
        self._responses = responses
        self._index = 0

    def complete(self, system: str, user: str) -> str:
        response = self._responses[min(self._index, len(self._responses) - 1)]
        self._index += 1
        return response


def _method_context() -> EntityContext:
    init_fn = FunctionModel(
        name="__init__",
        parameters=[
            ParameterModel(name="self"),
            ParameterModel(name="storage"),
        ],
        is_method=True,
        owner_class="OrderService",
    )
    create_fn = FunctionModel(
        name="create_order",
        parameters=[
            ParameterModel(name="self"),
            ParameterModel(name="customer"),
        ],
        returns="Order",
        is_method=True,
        owner_class="OrderService",
    )
    service_cls = ClassModel(name="OrderService", methods=[init_fn, create_fn])
    return EntityContext(
        entity_type="method",
        entity_name="OrderService.create_order",
        entity_id="services.py::OrderService.create_order",
        module_path="services.py",
        project_name="demo",
        signature="def create_order(self, customer: str) -> Order",
        function=create_fn,
        class_model=service_cls,
        module=ModuleModel(path="services.py", classes=[service_cls]),
    )


def _valid_response(examples: str) -> str:
    return f"""## Summary

Creates an order.

## Parameters

- `customer` (`str`) — customer name

## Returns

- `Order` — created order

## Raises

N/A

## Edge cases

N/A

## Side effects

N/A

## Examples

{examples}

## See also

N/A
"""


def test_pipeline_retries_on_blocking_examples() -> None:
    bad = _valid_response("```python\nOrderService().create_order('John')\n```")
    good = _valid_response("N/A")
    pipeline = EntityDocumentPipeline(MarkdownSectionParser(), MarkdownOutputFormatter())
    ctx = _method_context()
    llm = _SequenceLLM([bad, good])

    block, err, _ = pipeline.run(
        ctx,
        llm,
        "system",
        "user",
        "ru",
        max_retries=2,
        validation_config=ValidationConfig(retry_on_blocking=True),
    )

    assert err is None
    assert block is not None
    assert llm._index == 2
    assert "OrderService()" not in (block.examples or "")


def test_pipeline_strip_examples_fallback() -> None:
    bad = _valid_response("```python\nOrderService().create_order('John')\n```")
    pipeline = EntityDocumentPipeline(MarkdownSectionParser(), MarkdownOutputFormatter())
    ctx = _method_context()
    llm = _SequenceLLM([bad])

    block, err, _ = pipeline.run(
        ctx,
        llm,
        "system",
        "user",
        "ru",
        max_retries=0,
        validation_config=ValidationConfig(
            retry_on_blocking=False,
            blocking_fallback="strip_examples",
        ),
    )

    assert err is None
    assert block is not None
    assert block.examples == "N/A"
