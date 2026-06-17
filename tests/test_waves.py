from __future__ import annotations

from andocgen.call_graph.implementations.static import StaticCallGraphBuilder
from andocgen.generator.waves import group_into_waves
from andocgen.models.entities import (
    CallGraph,
    CallGraphEdge,
    CallGraphNode,
    EntityContext,
    FunctionModel,
    ModuleModel,
    ProjectModel,
    make_entity_id,
)


def _ctx(module: str, kind: str, name: str) -> EntityContext:
    eid = make_entity_id(module, kind, name)  # type: ignore[arg-type]
    return EntityContext(
        entity_type=kind,  # type: ignore[arg-type]
        entity_name=name,
        entity_id=eid,
        module_path=module,
        project_name="test",
        signature="",
    )


def test_waves_respect_callee_order() -> None:
    mod = "a.py"
    caller = _ctx(mod, "function", "caller")
    callee = _ctx(mod, "function", "callee")
    cls = _ctx(mod, "class", "MyClass")
    module = _ctx(mod, "module", mod)

    graph = CallGraph(
        nodes=[
            CallGraphNode(id=caller.entity_id, module=mod, name="caller", kind="function"),
            CallGraphNode(id=callee.entity_id, module=mod, name="callee", kind="function"),
        ],
        edges=[
            CallGraphEdge(caller_id=caller.entity_id, callee_name="callee", callee_id=callee.entity_id),
        ],
    )
    builder = StaticCallGraphBuilder()
    waves = group_into_waves([caller, callee, cls, module], graph, builder)

    fn_wave_indices = [
        i
        for i, wave in enumerate(waves)
        if any(c.entity_type in ("function", "method") for c in wave)
    ]
    assert callee in waves[fn_wave_indices[0]]
    assert caller in waves[fn_wave_indices[-1]]
    assert waves[-1] == [module]


def test_waves_from_call_graph_builder() -> None:
    fn_a = FunctionModel(name="a", calls=["b"])
    fn_b = FunctionModel(name="b")
    module = ModuleModel(path="m.py", functions=[fn_a, fn_b])
    project = ProjectModel(project_path="/tmp", modules=[module], project_name="t")

    builder = StaticCallGraphBuilder()
    graph = builder.build(project)
    contexts = [
        _ctx("m.py", "module", "m.py"),
        _ctx("m.py", "function", "a"),
        _ctx("m.py", "function", "b"),
    ]
    ordered = builder.order_entities(contexts, graph)
    waves = group_into_waves(ordered, graph, builder)
    flat = [c.entity_id for wave in waves for c in wave]
    assert flat.index(make_entity_id("m.py", "function", "b")) < flat.index(
        make_entity_id("m.py", "function", "a")
    )


def test_modules_grouped_in_single_wave() -> None:
    contexts = [
        _ctx("a.py", "module", "a.py"),
        _ctx("b.py", "module", "b.py"),
        _ctx("c.py", "module", "c.py"),
    ]
    waves = group_into_waves(contexts, CallGraph(), StaticCallGraphBuilder())
    assert len(waves) == 1
    assert len(waves[0]) == 3
    assert all(c.entity_type == "module" for c in waves[0])
