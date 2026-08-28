from __future__ import annotations

from andocgen.config import ValidationConfig
from andocgen.generator.entity_pipeline import EntityDocumentPipeline
from andocgen.generator.implementations.markdown_formatter import MarkdownOutputFormatter
from andocgen.generator.implementations.markdown_section_parser import MarkdownSectionParser
from andocgen.models.entities import (
    ClassModel,
    EntityContext,
    FunctionModel,
    ModuleModel,
    ParameterModel,
)


def test_fallback_blocks_emit_validation_warning() -> None:
    from andocgen.models.entities import IssueCategory, IssueLevel, ValidationIssue
    from andocgen.pipeline import _fallback_issues

    block = build_fallback_for_test()

    issues = _fallback_issues([block])

    assert issues == [
        ValidationIssue(
            level=IssueLevel.WARNING,
            category=IssueCategory.GENERATION,
            message="fallback_generated",
            module_path="calc.py",
            entity_type="function",
            entity_name="add",
        )
    ]


def build_fallback_for_test():
    from andocgen.models.entities import DocBlock

    return DocBlock(
        entity_type="function",
        entity_name="add",
        module_path="calc.py",
        fallback=True,
    )


class _BrokenLLM:
    def complete(self, system: str, user: str) -> str:
        return "not parseable"


def test_entity_pipeline_returns_fallback_function_block_after_parse_failures() -> None:
    fn = FunctionModel(
        name="add",
        parameters=[ParameterModel("a", "int"), ParameterModel("b", "int")],
        returns="int",
        docstring="Add two numbers.",
    )
    ctx = EntityContext(
        entity_type="function",
        entity_name="add",
        entity_id="calc.py::add",
        module_path="calc.py",
        project_name="demo",
        signature=fn.signature(),
        source_docstring=fn.docstring,
        function=fn,
    )
    pipeline = EntityDocumentPipeline(MarkdownSectionParser(), MarkdownOutputFormatter())

    block, err, _ = pipeline.run(
        ctx,
        _BrokenLLM(),
        "system",
        "user",
        "ru",
        max_retries=0,
        validation_config=ValidationConfig(),
    )

    assert err is None
    assert block is not None
    assert block.fallback is True
    assert block.summary == "Add two numbers."
    assert [p.name for p in block.parameters or []] == ["a", "b"]
    assert block.returns is not None
    assert block.returns.type == "int"
    assert "def add" in block.content


def test_entity_pipeline_returns_fallback_class_block_after_parse_failures() -> None:
    cls = ClassModel(
        name="User",
        docstring="Stores user data.",
        field_defs=[ParameterModel("name", "str")],
    )
    ctx = EntityContext(
        entity_type="class",
        entity_name="User",
        entity_id="models.py::User",
        module_path="models.py",
        project_name="demo",
        signature="class User",
        source_docstring=cls.docstring,
        class_model=cls,
    )
    pipeline = EntityDocumentPipeline(MarkdownSectionParser(), MarkdownOutputFormatter())

    block, err, _ = pipeline.run(
        ctx,
        _BrokenLLM(),
        "system",
        "user",
        "ru",
        max_retries=0,
        validation_config=ValidationConfig(),
    )

    assert err is None
    assert block is not None
    assert block.fallback is True
    assert [field.name for field in block.fields or []] == ["name"]
    assert "class User" in block.content


def test_entity_pipeline_returns_fallback_module_block_after_parse_failures() -> None:
    module = ModuleModel(path="pkg/__init__.py", docstring="Package root.", exports=["User"])
    ctx = EntityContext(
        entity_type="module",
        entity_name="pkg/__init__.py",
        entity_id="pkg/__init__.py::module",
        module_path="pkg/__init__.py",
        project_name="demo",
        source_docstring=module.docstring,
        module=module,
    )
    pipeline = EntityDocumentPipeline(MarkdownSectionParser(), MarkdownOutputFormatter())

    block, err, _ = pipeline.run(
        ctx,
        _BrokenLLM(),
        "system",
        "user",
        "ru",
        max_retries=0,
        validation_config=ValidationConfig(),
    )

    assert err is None
    assert block is not None
    assert block.fallback is True
    assert [export.name for export in block.exports or []] == ["User"]
