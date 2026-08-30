from __future__ import annotations

import tomllib
from pathlib import Path


def test_mypy_is_configured_as_project_tooling() -> None:
    payload = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert any(dep.startswith("mypy>=") for dep in payload["project"]["optional-dependencies"]["dev"])
    assert payload["tool"]["mypy"]["python_version"] == "3.11"
    assert payload["tool"]["mypy"]["packages"] == ["andocgen"]
