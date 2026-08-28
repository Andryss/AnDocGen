from __future__ import annotations

import json

from andocgen.models.entities import DocBlock, ModuleModel
from andocgen.output.implementations.json_cache import JsonCacheStore


def test_json_cache_stores_source_and_doc_hashes(tmp_path) -> None:
    module = ModuleModel(path="a.py", content_hash="source-hash")
    block = DocBlock(
        entity_type="function",
        entity_name="add",
        module_path="a.py",
        content="doc content",
    )

    JsonCacheStore().update(tmp_path / "cache", [module], [block])

    payload = json.loads((tmp_path / "cache" / "checksums.json").read_text(encoding="utf-8"))
    assert payload["files"]["a.py"]["source_hash"] == "source-hash"
    assert payload["files"]["a.py"]["doc_hash"]
    assert JsonCacheStore().load(tmp_path / "cache") == {"a.py": "source-hash"}
