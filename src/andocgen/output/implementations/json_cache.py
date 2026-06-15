from __future__ import annotations

import json
from pathlib import Path

from andocgen.models.entities import ModuleModel


class JsonCacheStore:
    def load(self, cache_dir: Path) -> dict[str, str]:
        cache_path = cache_dir / "checksums.json"
        legacy = cache_dir.parent / ".andocgen_cache.json"
        if cache_path.exists():
            return json.loads(cache_path.read_text(encoding="utf-8"))
        if legacy.exists():
            return json.loads(legacy.read_text(encoding="utf-8"))
        return {}

    def update(self, cache_dir: Path, modules: list[ModuleModel]) -> None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / "checksums.json"
        cache: dict[str, str] = {}
        if cache_path.exists():
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        for module in modules:
            cache[module.path] = module.content_hash
        cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")
