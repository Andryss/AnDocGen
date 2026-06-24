from __future__ import annotations

from andocgen.call_graph.factory import create_call_graph_builder
from andocgen.config import CallGraphConfig, ContextConfig, ExtractionConfig
from andocgen.context.factory import create_context_components
from andocgen.models.entities import ProjectModel
from andocgen.parser.factory import create_parser

from tests.conftest import FIXTURE_PROJECT_API


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
