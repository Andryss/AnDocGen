from __future__ import annotations

import json

from andocgen.io.json_utils import append_jsonl, read_json_object, write_json


def test_json_utils_read_and_write_json_objects(tmp_path) -> None:
    path = tmp_path / "payload.json"

    assert read_json_object(path, default={"files": {}}) == {"files": {}}

    write_json(path, {"answer": 42})

    assert read_json_object(path) == {"answer": 42}
    assert json.loads(path.read_text(encoding="utf-8")) == {"answer": 42}


def test_json_utils_appends_jsonl(tmp_path) -> None:
    path = tmp_path / "events.jsonl"

    append_jsonl(path, {"event": "start"})
    append_jsonl(path, {"event": "done"})

    assert path.read_text(encoding="utf-8").splitlines() == [
        '{"event": "start"}',
        '{"event": "done"}',
    ]
