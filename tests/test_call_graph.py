from __future__ import annotations

from andocgen.call_graph.factory import create_call_graph_builder
from andocgen.config import CallGraphConfig, ContextConfig, ExtractionConfig
from andocgen.context.factory import create_context_components
from andocgen.models.entities import ProjectModel
from andocgen.parser.factory import create_parser
from tests.conftest import FIXTURE_PROJECT_API, FIXTURE_PROJECT_SELF_CALL, FIXTURE_PROJECT_UNKNOWN_CALL


def test_cross_module_call_resolution() -> None:
    parser = create_parser(ExtractionConfig())
    modules = []
    for rel in ("storage.py", "handlers.py"):
        result = parser.parse(FIXTURE_PROJECT_API / rel, FIXTURE_PROJECT_API)
        assert result.module is not None
        modules.append(result.module)

    project = ProjectModel(project_path=str(FIXTURE_PROJECT_API), modules=modules)
    call_graph_builder = create_call_graph_builder(CallGraphConfig())
    graph = call_graph_builder.build(project)

    create_user_id = "handlers.py::UserHandler.create_user"
    normalize_id = "storage.py::normalize_email"
    edge_targets = {
        e.callee_id
        for e in graph.edges
        if e.caller_id == create_user_id
    }
    assert normalize_id in edge_targets

    context_builder = create_context_components(ContextConfig()).context_builder
    contexts = context_builder.build(project, ContextConfig())
    ordered = call_graph_builder.order_entities(contexts, graph)
    fn_ids = [c.entity_id for c in ordered if c.entity_type in ("function", "method")]
    assert fn_ids.index(normalize_id) < fn_ids.index(create_user_id)


def test_unknown_local_call_remains_unresolved() -> None:
    path = FIXTURE_PROJECT_UNKNOWN_CALL / "mod.py"
    parser = create_parser(ExtractionConfig())
    result = parser.parse(path, FIXTURE_PROJECT_UNKNOWN_CALL)
    assert result.module is not None

    project = ProjectModel(project_path=str(FIXTURE_PROJECT_UNKNOWN_CALL), modules=[result.module])
    graph = create_call_graph_builder(CallGraphConfig()).build(project)

    edge = graph.edges[0]
    assert edge.callee_name == "missing"
    assert edge.callee_id is None


def test_method_call_on_self_resolves_to_method() -> None:
    path = FIXTURE_PROJECT_SELF_CALL / "service.py"
    parser = create_parser(ExtractionConfig())
    result = parser.parse(path, FIXTURE_PROJECT_SELF_CALL)
    assert result.module is not None

    project = ProjectModel(project_path=str(FIXTURE_PROJECT_SELF_CALL), modules=[result.module])
    graph = create_call_graph_builder(CallGraphConfig()).build(project)
    edge_targets = {edge.callee_id for edge in graph.edges if edge.caller_id == "service.py::Service.run"}

    assert "service.py::Service.helper" in edge_targets
