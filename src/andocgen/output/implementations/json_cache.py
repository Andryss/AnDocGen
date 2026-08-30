from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from andocgen.io.json_utils import read_json_object, write_json
from andocgen.models.entities import CallGraph, DocBlock, ModuleModel, make_entity_id
from andocgen.models.iteration import module_entity_ids


class JsonCacheStore:
    def load(self, cache_dir: Path) -> dict[str, str]:
        cache_path = cache_dir / "checksums.json"
        payload = read_json_object(cache_path)
        files = payload.get("files", {})
        if not isinstance(files, dict):
            return {}
        return {
            path: item.get("source_hash", "")
            for path, item in files.items()
            if isinstance(path, str) and isinstance(item, dict)
        }

    def load_snapshot(self, cache_dir: Path):
        from andocgen.generation_plan import cache_snapshot_from_raw

        cache_path = cache_dir / "checksums.json"
        return cache_snapshot_from_raw(read_json_object(cache_path))

    def update(
        self,
        cache_dir: Path,
        modules: list[ModuleModel],
        blocks: list[DocBlock] | None = None,
        graph: CallGraph | None = None,
    ) -> None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / "checksums.json"
        files: dict[str, dict[str, str]] = {}
        entities: dict[str, dict[str, str]] = {}
        if cache_path.exists():
            payload = read_json_object(cache_path)
            raw_files = payload.get("files", {}) if isinstance(payload, dict) else {}
            if isinstance(raw_files, dict):
                files = {
                    path: dict(item)
                    for path, item in raw_files.items()
                    if isinstance(item, dict)
                }
            raw_entities = payload.get("entities", {}) if isinstance(payload, dict) else {}
            if isinstance(raw_entities, dict):
                entities = {
                    entity_id: dict(item)
                    for entity_id, item in raw_entities.items()
                    if isinstance(item, dict)
                }
        doc_hashes = _doc_hashes_by_module(blocks or [])
        doc_hashes_by_entity = _doc_hashes_by_entity(blocks or [])
        dependency_hashes = _dependency_hashes(graph, doc_hashes_by_entity) if graph else {}
        for module in modules:
            files[module.path] = {
                "source_hash": module.content_hash,
                "doc_hash": doc_hashes.get(module.path, files.get(module.path, {}).get("doc_hash", "")),
            }
            for entity_id in module_entity_ids(module):
                previous = entities.get(entity_id, {})
                entities[entity_id] = {
                    "source_hash": module.content_hash,
                    "doc_hash": doc_hashes_by_entity.get(entity_id, previous.get("doc_hash", "")),
                    "dependency_hash": dependency_hashes.get(entity_id, previous.get("dependency_hash", "")),
                }
        source_hashes = {module.path: module.content_hash for module in modules}
        for block in blocks or []:
            entity_id = make_entity_id(block.module_path, block.entity_type, block.entity_name)
            previous = entities.get(entity_id, {})
            entities[entity_id] = {
                "source_hash": source_hashes.get(block.module_path, previous.get("source_hash", "")),
                "doc_hash": doc_hashes_by_entity.get(entity_id, previous.get("doc_hash", "")),
                "dependency_hash": dependency_hashes.get(entity_id, previous.get("dependency_hash", "")),
            }
        write_json(cache_path, {"files": files, "entities": entities})


def _doc_hashes_by_module(blocks: list[DocBlock]) -> dict[str, str]:
    grouped: dict[str, list[str]] = {}
    for block in blocks:
        grouped.setdefault(block.module_path, []).append(docblock_hash(block))
    return {
        module_path: hashlib.sha256("\n".join(sorted(items)).encode("utf-8")).hexdigest()
        for module_path, items in grouped.items()
    }


def _doc_hashes_by_entity(blocks: list[DocBlock]) -> dict[str, str]:
    return {
        make_entity_id(block.module_path, block.entity_type, block.entity_name): docblock_hash(block)
        for block in blocks
    }


def docblock_hash(block: DocBlock) -> str:
    payload = asdict(block)
    payload.pop("content", None)
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _dependency_hashes(graph: CallGraph, doc_hashes_by_entity: dict[str, str]) -> dict[str, str]:
    dependencies: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.callee_id is None:
            continue
        callee_hash = doc_hashes_by_entity.get(edge.callee_id)
        if callee_hash:
            dependencies.setdefault(edge.caller_id, []).append(callee_hash)
    return {
        entity_id: hashlib.sha256("\n".join(sorted(hashes)).encode("utf-8")).hexdigest()
        for entity_id, hashes in dependencies.items()
    }
