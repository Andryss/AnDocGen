from __future__ import annotations

from pathlib import Path

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


class StaticCallGraphBuilder:
    def build(self, project: ProjectModel) -> CallGraph:
        graph = CallGraph()
        module_index = _build_module_index(project)
        import_maps = {m.path: _build_import_map(m, module_index) for m in project.modules}

        for module in project.modules:
            for fn in _iter_functions(module):
                node_id = _function_node_id(module.path, fn)
                graph.nodes.append(
                    CallGraphNode(
                        id=node_id,
                        module=module.path,
                        name=fn.qualified_name(),
                        kind="method" if fn.is_method else "function",
                        class_name=fn.owner_class,
                    )
                )

        module_deps: dict[str, set[str]] = {m.path: set() for m in project.modules}

        for module in project.modules:
            import_map = import_maps[module.path]
            for fn in _iter_functions(module):
                caller_id = _function_node_id(module.path, fn)
                for call in fn.calls:
                    callee_id = _resolve_call(call, module.path, import_map, module_index)
                    graph.edges.append(
                        CallGraphEdge(
                            caller_id=caller_id,
                            callee_name=call,
                            callee_id=callee_id,
                        )
                    )
                    if callee_id:
                        callee_module = callee_id.split("::", 1)[0]
                        if callee_module != module.path:
                            module_deps[module.path].add(callee_module)

        graph.module_dependencies = {k: sorted(v) for k, v in module_deps.items()}
        project.call_graph = graph
        return graph

    def order_entities(self, contexts: list[EntityContext], graph: CallGraph) -> list[EntityContext]:
        fn_method = [c for c in contexts if c.entity_type in ("function", "method")]
        classes = [c for c in contexts if c.entity_type == "class"]
        modules = [c for c in contexts if c.entity_type == "module"]

        fn_ids = {c.entity_id for c in fn_method}
        adjacency: dict[str, list[str]] = {cid: [] for cid in fn_ids}
        indegree: dict[str, int] = {cid: 0 for cid in fn_ids}

        for edge in graph.edges:
            if edge.caller_id in fn_ids and edge.callee_id and edge.callee_id in fn_ids:
                adjacency[edge.callee_id].append(edge.caller_id)
                indegree[edge.caller_id] += 1

        queue = sorted([cid for cid, deg in indegree.items() if deg == 0])
        ordered_ids: list[str] = []
        while queue:
            current = queue.pop(0)
            ordered_ids.append(current)
            for nxt in sorted(adjacency.get(current, [])):
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
                    queue.sort()

        if len(ordered_ids) < len(fn_ids):
            remaining = sorted(fn_ids - set(ordered_ids))
            ordered_ids.extend(remaining)

        ctx_by_id = {c.entity_id: c for c in fn_method}
        ordered_fn = [ctx_by_id[cid] for cid in ordered_ids if cid in ctx_by_id]
        return ordered_fn + classes + modules

    def get_callee_ids(self, entity_id: str, graph: CallGraph) -> list[str]:
        return [e.callee_id for e in graph.edges if e.caller_id == entity_id and e.callee_id]

    def get_unresolved_calls(self, entity_id: str, graph: CallGraph) -> list[str]:
        return [e.callee_name for e in graph.edges if e.caller_id == entity_id and not e.callee_id]


def _iter_functions(module: ModuleModel) -> list[FunctionModel]:
    fns = list(module.functions)
    for cls in module.classes:
        fns.extend(cls.methods)
    return fns


def _function_node_id(module_path: str, fn: FunctionModel) -> str:
    return make_entity_id(module_path, "method" if fn.is_method else "function", fn.qualified_name())


def _build_module_index(project: ProjectModel) -> dict[str, str]:
    index: dict[str, str] = {}
    for module in project.modules:
        path = Path(module.path)
        stem = path.stem
        index[stem] = module.path
        parts = path.with_suffix("").parts
        if parts:
            index[".".join(parts)] = module.path
            index[parts[-1]] = module.path
        pkg_parts = list(parts)
        if stem == "__init__":
            pkg_parts = pkg_parts[:-1]
            if pkg_parts:
                index[".".join(pkg_parts)] = module.path
    return index


def _build_import_map(module: ModuleModel, module_index: dict[str, str]) -> dict[str, str]:
    import_map: dict[str, str] = {}
    module_dir = str(Path(module.path).parent).replace("\\", "/")

    for imp in module.imports:
        if imp.level > 0:
            base_parts = module_dir.split("/") if module_dir != "." else []
            if imp.level > 1:
                base_parts = base_parts[: -(imp.level - 1)]
            rel_module = ".".join(p for p in [*base_parts, imp.module or ""] if p)
        else:
            rel_module = imp.module

        resolved = module_index.get(rel_module) or module_index.get(rel_module.split(".")[-1])
        if not resolved and imp.module:
            candidate = imp.module.replace(".", "/") + ".py"
            resolved = module_index.get(Path(candidate).stem) or module_index.get(candidate)

        if imp.names:
            for name in imp.names:
                alias = name.split(" as ")[0].strip() if " as " in name else name
                if resolved:
                    import_map[alias] = resolved
        elif resolved:
            alias = Path(resolved).stem
            import_map[alias] = resolved

    return import_map


def _resolve_call(
    call: str,
    module_path: str,
    import_map: dict[str, str],
    module_index: dict[str, str],
) -> str | None:
    if "." in call:
        parts = call.split(".")
        base = parts[0]
        attr = parts[-1]
        if base in import_map:
            target_module = import_map[base]
            return _find_entity_in_module(target_module, attr, module_index)
        if len(parts) == 2:
            return _find_entity_in_module(module_path, call, module_index)
        return None

    if call in import_map:
        target_module = import_map[call]
        return _find_entity_in_module(target_module, call, module_index)

    return _find_entity_in_module(module_path, call, module_index)


def _find_entity_in_module(module_path: str, name: str, module_index: dict[str, str]) -> str | None:
    if "." in name:
        class_name, method_name = name.rsplit(".", 1)
        return make_entity_id(module_path, "method", f"{class_name}.{method_name}")
    return make_entity_id(module_path, "function", name)
