from __future__ import annotations

from andocgen.models.entities import ClassModel, FunctionModel, ModuleModel, ProjectModel
from andocgen.models.iteration import (
    entity_module_map,
    iter_module_functions,
    iter_project_functions,
    module_entity_ids,
)


def test_iteration_helpers_preserve_entity_order_and_ids() -> None:
    method = FunctionModel(name="run", is_method=True, owner_class="Worker")
    module = ModuleModel(
        path="pkg/service.py",
        functions=[FunctionModel(name="build")],
        classes=[ClassModel(name="Worker", methods=[method])],
    )

    assert [fn.qualified_name() for fn in iter_module_functions(module)] == ["build", "Worker.run"]
    assert [fn.qualified_name() for _, fn in iter_project_functions(ProjectModel("pkg", [module]))] == [
        "build",
        "Worker.run",
    ]
    assert module_entity_ids(module) == [
        "pkg/service.py::module",
        "pkg/service.py::build",
        "pkg/service.py::Worker",
        "pkg/service.py::Worker.run",
    ]
    assert entity_module_map([module]) == {
        "pkg/service.py::module": "pkg/service.py",
        "pkg/service.py::build": "pkg/service.py",
        "pkg/service.py::Worker": "pkg/service.py",
        "pkg/service.py::Worker.run": "pkg/service.py",
    }
