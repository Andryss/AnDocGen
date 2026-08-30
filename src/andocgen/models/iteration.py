from __future__ import annotations

from collections.abc import Iterator

from andocgen.models.entities import FunctionModel, ModuleModel, ProjectModel, make_entity_id


def iter_module_functions(module: ModuleModel) -> Iterator[FunctionModel]:
    yield from module.functions
    for cls in module.classes:
        yield from cls.methods


def iter_project_functions(project: ProjectModel) -> Iterator[tuple[ModuleModel, FunctionModel]]:
    for module in project.modules:
        for function in iter_module_functions(module):
            yield module, function


def module_entity_ids(module: ModuleModel) -> list[str]:
    ids = [make_entity_id(module.path, "module", "module")]
    ids.extend(make_entity_id(module.path, "function", fn.name) for fn in module.functions)
    for cls in module.classes:
        ids.append(make_entity_id(module.path, "class", cls.name))
        ids.extend(make_entity_id(module.path, "method", method.qualified_name()) for method in cls.methods)
    return ids


def entity_module_map(modules: list[ModuleModel]) -> dict[str, str]:
    result: dict[str, str] = {}
    for module in modules:
        for entity_id in module_entity_ids(module):
            result[entity_id] = module.path
    return result
