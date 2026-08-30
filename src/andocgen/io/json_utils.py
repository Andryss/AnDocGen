from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json_object(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return dict(default or {})
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return dict(default or {})
    return payload


def write_json(path: Path, payload: object, *, indent: int = 2) -> None:
    path.write_text(json.dumps(payload, indent=indent, ensure_ascii=False), encoding="utf-8")


def append_jsonl(path: Path, payload: object) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
