from __future__ import annotations

from andocgen.context.doc_brief_registry import DocBriefRegistry
from andocgen.context.implementations.default_context import DefaultContextBuilder
from andocgen.context.implementations.sectioned_prompt import SectionedPromptBuilder
from andocgen.models.entities import (
    CallGraph,
    ClassModel,
    EntityContext,
    FunctionModel,
    ModuleModel,
    ProjectModel,
    make_entity_id,
)


def test_brief_line_format() -> None:
    registry = DocBriefRegistry()
    registry.register("m.py::foo", "Adds numbers.", "def foo(a: int) -> int", "function")
    assert registry.brief_line("m.py::foo") == "- `def foo(a: int) -> int` — Adds numbers."


def test_attach_callee_briefs_not_full_markdown() -> None:
    registry = DocBriefRegistry()
    registry.register("m.py::helper", "Helper fn.", "def helper()", "function")
    ctx = EntityContext(
        entity_type="function",
        entity_name="main",
        entity_id="m.py::main",
        module_path="m.py",
        project_name="demo",
    )
    builder = DefaultContextBuilder()
    builder.attach_callee_briefs(ctx, registry, ["m.py::helper"], [])
    assert len(ctx.called_entities_docs) == 1
    assert "Helper fn." in ctx.called_entities_docs[0].content
    assert "## Summary" not in ctx.called_entities_docs[0].content


def test_attach_class_method_briefs() -> None:
    registry = DocBriefRegistry()
    method_id = make_entity_id("m.py", "method", "Svc.run")
    registry.register(method_id, "Runs service.", "def run(self) -> None", "method")
    cls = ClassModel(
        name="Svc",
        methods=[FunctionModel(name="run", is_method=True, owner_class="Svc")],
    )
    ctx = EntityContext(
        entity_type="class",
        entity_name="Svc",
        entity_id="m.py::Svc",
        module_path="m.py",
        project_name="demo",
        class_model=cls,
    )
    DefaultContextBuilder().attach_class_method_briefs(ctx, registry)
    assert len(ctx.class_member_docs) == 1
    assert "Runs service." in ctx.class_member_docs[0].content


def test_class_prompt_excludes_source_body() -> None:
    ctx = EntityContext(
        entity_type="class",
        entity_name="Big",
        entity_id="m.py::Big",
        module_path="m.py",
        project_name="demo",
        source_body="class Big:\n" + "    pass\n" * 500,
        class_member_docs=[],
    )
    prompt = SectionedPromptBuilder().build_user_message(ctx, max_chars=32000)
    assert "pass\n" * 10 not in prompt
    assert "## Source" in prompt


def test_module_dependency_briefs() -> None:
    registry = DocBriefRegistry()
    dep_id = make_entity_id("other.py", "module", "module")
    registry.register(dep_id, "Other module.", "", "module")
    module = ModuleModel(path="m.py")
    graph = CallGraph(module_dependencies={"m.py": ["other.py"]})
    ctx = EntityContext(
        entity_type="module",
        entity_name="m.py",
        entity_id="m.py::module",
        module_path="m.py",
        project_name="demo",
        module=module,
    )
    DefaultContextBuilder().attach_module_dependency_briefs(ctx, registry, graph)
    assert len(ctx.module_dependency_docs) == 1
    assert "Other module." in ctx.module_dependency_docs[0].content
