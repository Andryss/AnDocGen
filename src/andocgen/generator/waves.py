from __future__ import annotations

from andocgen.call_graph.base import CallGraphBuilder
from andocgen.models.entities import CallGraph, EntityContext


def group_into_waves(
    contexts: list[EntityContext],
    graph: CallGraph,
    call_graph_builder: CallGraphBuilder,
) -> list[list[EntityContext]]:
    fn_method = [c for c in contexts if c.entity_type in ("function", "method")]
    classes = [c for c in contexts if c.entity_type == "class"]
    modules = [c for c in contexts if c.entity_type == "module"]

    fn_ids = {c.entity_id for c in fn_method}
    deps: dict[str, set[str]] = {}
    for ctx in fn_method:
        callee_ids = call_graph_builder.get_callee_ids(ctx.entity_id, graph)
        deps[ctx.entity_id] = {cid for cid in callee_ids if cid in fn_ids}

    waves: list[list[EntityContext]] = []
    ready: set[str] = set()
    remaining = {c.entity_id: c for c in fn_method}

    while remaining:
        wave = [ctx for eid, ctx in remaining.items() if deps[eid].issubset(ready)]
        if not wave:
            wave = list(remaining.values())
        waves.append(wave)
        for ctx in wave:
            remaining.pop(ctx.entity_id)
            ready.add(ctx.entity_id)

    if classes:
        waves.append(classes)
    for module in modules:
        waves.append([module])

    return waves
