from __future__ import annotations

import json

from andocgen.models.entities import CallGraph, CallGraphEdge, DocBlock, ModuleModel
from andocgen.output.implementations.json_cache import JsonCacheStore


def test_json_cache_stores_source_and_doc_hashes(tmp_path) -> None:
    module = ModuleModel(path="a.py", content_hash="source-hash")
    block = DocBlock(
        entity_type="function",
        entity_name="add",
        module_path="a.py",
        content="doc content",
    )

    graph = CallGraph(
        edges=[
            CallGraphEdge(
                caller_id="a.py::caller",
                callee_name="add",
                callee_id="a.py::add",
            )
        ]
    )
    caller = DocBlock(
        entity_type="function",
        entity_name="caller",
        module_path="a.py",
        content="caller doc",
    )

    JsonCacheStore().update(tmp_path / "cache", [module], [block, caller], graph)

    payload = json.loads((tmp_path / "cache" / "checksums.json").read_text(encoding="utf-8"))
    assert payload["files"]["a.py"]["source_hash"] == "source-hash"
    assert payload["files"]["a.py"]["doc_hash"]
    assert payload["entities"]["a.py::add"]["source_hash"] == "source-hash"
    assert payload["entities"]["a.py::add"]["doc_hash"]
    assert payload["entities"]["a.py::caller"]["dependency_hash"]
    assert JsonCacheStore().load(tmp_path / "cache") == {"a.py": "source-hash"}
