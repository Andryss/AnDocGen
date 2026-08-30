from __future__ import annotations

from dataclasses import dataclass, field

from andocgen.models.entities import CallGraph, DocBlock, ModuleModel, ProjectModel, make_entity_id
from andocgen.models.iteration import entity_module_map
from andocgen.output.implementations.json_cache import docblock_hash

GenerationReason = str


@dataclass
class CacheSnapshot:
    files: dict[str, dict[str, str]] = field(default_factory=dict)
    entities: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class GenerationPlan:
    generated_entity_ids: list[str] = field(default_factory=list)
    skipped_entity_ids: list[str] = field(default_factory=list)
    reasons: dict[str, GenerationReason] = field(default_factory=dict)

    @property
    def affected_module_paths(self) -> set[str]:
        return {entity_id.split("::", 1)[0] for entity_id in self.generated_entity_ids}


def build_generation_plan(project: ProjectModel, graph: CallGraph, cache: CacheSnapshot) -> GenerationPlan:
    entity_modules = entity_module_map(project.modules)
    known_entity_ids = set(entity_modules)
    generated: set[str] = set()
    reasons: dict[str, GenerationReason] = {}

    for entity_id, module_path in entity_modules.items():
        cached = cache.entities.get(entity_id)
        if cached is None:
            generated.add(entity_id)
            reasons[entity_id] = "missing_cache"
            continue
        source_hash = _module_hash(project.modules, module_path)
        if cached.get("source_hash") != source_hash:
            generated.add(entity_id)
            reasons[entity_id] = "source_changed"

    queue = list(generated)
    while queue:
        current = queue.pop(0)
        for edge in graph.edges:
            if edge.callee_id != current:
                continue
            if edge.caller_id not in known_entity_ids or edge.caller_id in generated:
                continue
            generated.add(edge.caller_id)
            reasons[edge.caller_id] = "dependency_changed"
            queue.append(edge.caller_id)

    ordered_generated = sorted(generated)
    return GenerationPlan(
        generated_entity_ids=ordered_generated,
        skipped_entity_ids=sorted(known_entity_ids - generated),
        reasons={entity_id: reasons[entity_id] for entity_id in ordered_generated},
    )


def changed_doc_modules(blocks: list[DocBlock], cache: CacheSnapshot) -> set[str]:
    changed: set[str] = set()
    for block in blocks:
        entity_id = make_entity_id(block.module_path, block.entity_type, block.entity_name)
        cached = cache.entities.get(entity_id)
        if cached is None or cached.get("doc_hash") != docblock_hash(block):
            changed.add(block.module_path)
    return changed


def cache_snapshot_from_raw(raw: dict[str, object]) -> CacheSnapshot:
    files = raw.get("files", {}) if isinstance(raw, dict) else {}
    entities = raw.get("entities", {}) if isinstance(raw, dict) else {}
    return CacheSnapshot(
        files={k: dict(v) for k, v in files.items() if isinstance(k, str) and isinstance(v, dict)}
        if isinstance(files, dict)
        else {},
        entities={k: dict(v) for k, v in entities.items() if isinstance(k, str) and isinstance(v, dict)}
        if isinstance(entities, dict)
        else {},
    )


def _module_hash(modules: list[ModuleModel], module_path: str) -> str:
    for module in modules:
        if module.path == module_path:
            return module.content_hash
    return ""
