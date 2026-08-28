from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from andocgen.models.entities import DocBlock, ModuleModel


class JsonCacheStore:
    def load(self, cache_dir: Path) -> dict[str, str]:
        cache_path = cache_dir / "checksums.json"
        if cache_path.exists():
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
            files = payload.get("files", {}) if isinstance(payload, dict) else {}
            return {
                path: item.get("source_hash", "")
                for path, item in files.items()
                if isinstance(item, dict)
            }
        return {}

    def update(self, cache_dir: Path, modules: list[ModuleModel], blocks: list[DocBlock] | None = None) -> None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / "checksums.json"
        files: dict[str, dict[str, str]] = {}
        if cache_path.exists():
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
            raw_files = payload.get("files", {}) if isinstance(payload, dict) else {}
            if isinstance(raw_files, dict):
                files = {
                    path: dict(item)
                    for path, item in raw_files.items()
                    if isinstance(item, dict)
                }
        doc_hashes = _doc_hashes_by_module(blocks or [])
        for module in modules:
            files[module.path] = {
                "source_hash": module.content_hash,
                "doc_hash": doc_hashes.get(module.path, files.get(module.path, {}).get("doc_hash", "")),
            }
        cache_path.write_text(
            json.dumps({"files": files}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


def _doc_hashes_by_module(blocks: list[DocBlock]) -> dict[str, str]:
    grouped: dict[str, list[str]] = {}
    for block in blocks:
        grouped.setdefault(block.module_path, []).append(json.dumps(asdict(block), sort_keys=True, ensure_ascii=False))
    return {
        module_path: hashlib.sha256("\n".join(sorted(items)).encode("utf-8")).hexdigest()
        for module_path, items in grouped.items()
    }
