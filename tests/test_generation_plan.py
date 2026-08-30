from __future__ import annotations

from andocgen.call_graph.implementations.static import StaticCallGraphBuilder
from andocgen.generation_plan import CacheSnapshot, build_generation_plan, changed_doc_modules
from andocgen.models.entities import (
    DocBlock,
    FunctionModel,
    ImportModel,
    ModuleModel,
    ProjectModel,
    make_entity_id,
)
from andocgen.output.implementations.json_cache import docblock_hash


def _project() -> ProjectModel:
    return ProjectModel(
        project_path="demo",
        modules=[
            ModuleModel(
                path="storage.py",
                content_hash="storage-v1",
                functions=[FunctionModel(name="normalize_email")],
            ),
            ModuleModel(
                path="handlers.py",
                content_hash="handlers-v1",
                imports=[ImportModel(module="storage", names=["normalize_email"])],
                functions=[FunctionModel(name="create_user", calls=["normalize_email"])],
            ),
            ModuleModel(
                path="other.py",
                content_hash="other-v1",
                functions=[FunctionModel(name="unrelated")],
            ),
        ],
    )


def _snapshot(project: ProjectModel) -> CacheSnapshot:
    return CacheSnapshot(
        files={
            module.path: {"source_hash": module.content_hash, "doc_hash": f"{module.path}-doc"}
            for module in project.modules
        },
        entities={
            make_entity_id(module.path, "module", "module"): {
                "source_hash": module.content_hash,
                "doc_hash": f"{module.path}::module-doc",
                "dependency_hash": "",
            }
            for module in project.modules
        }
        | {
            make_entity_id(module.path, "function", fn.name): {
                "source_hash": module.content_hash,
                "doc_hash": f"{module.path}::{fn.name}-doc",
                "dependency_hash": "",
            }
            for module in project.modules
            for fn in module.functions
        },
    )


def test_generation_plan_skips_unchanged_entities() -> None:
    project = _project()
    graph = StaticCallGraphBuilder().build(project)
    snapshot = _snapshot(project)

    plan = build_generation_plan(project, graph, snapshot)

    assert plan.generated_entity_ids == []
    assert set(plan.skipped_entity_ids) == set(snapshot.entities)


def test_generation_plan_regenerates_changed_leaf_and_caller() -> None:
    project = _project()
    project.modules[0].content_hash = "storage-v2"
    graph = StaticCallGraphBuilder().build(project)
    snapshot = _snapshot(_project())

    plan = build_generation_plan(project, graph, snapshot)

    normalize_id = make_entity_id("storage.py", "function", "normalize_email")
    caller_id = make_entity_id("handlers.py", "function", "create_user")
    unrelated_id = make_entity_id("other.py", "function", "unrelated")
    assert normalize_id in plan.generated_entity_ids
    assert caller_id in plan.generated_entity_ids
    assert unrelated_id in plan.skipped_entity_ids
    assert plan.reasons[normalize_id] == "source_changed"
    assert plan.reasons[caller_id] == "dependency_changed"


def test_generation_plan_missing_cache_regenerates_only_affected_entities() -> None:
    project = _project()
    graph = StaticCallGraphBuilder().build(project)
    snapshot = _snapshot(project)
    missing_id = make_entity_id("storage.py", "function", "normalize_email")
    del snapshot.entities[missing_id]

    plan = build_generation_plan(project, graph, snapshot)

    caller_id = make_entity_id("handlers.py", "function", "create_user")
    unrelated_id = make_entity_id("other.py", "function", "unrelated")
    assert missing_id in plan.generated_entity_ids
    assert caller_id in plan.generated_entity_ids
    assert unrelated_id in plan.skipped_entity_ids
    assert plan.reasons[missing_id] == "missing_cache"
    assert plan.reasons[caller_id] == "dependency_changed"


def test_unchanged_docblock_hash_does_not_trigger_module_rewrite() -> None:
    block = DocBlock(entity_type="function", entity_name="add", module_path="calc.py", summary="Adds numbers.")
    entity_id = make_entity_id("calc.py", "function", "add")
    snapshot = CacheSnapshot(
        files={"calc.py": {"source_hash": "src", "doc_hash": "module-doc"}},
        entities={entity_id: {"source_hash": "src", "doc_hash": docblock_hash(block), "dependency_hash": ""}},
    )

    assert changed_doc_modules([block], snapshot) == set()

    block.summary = "Adds numeric values."

    assert changed_doc_modules([block], snapshot) == {"calc.py"}
