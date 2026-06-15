from __future__ import annotations

from pathlib import Path
from typing import Protocol

from andocgen.config import DiscoveryConfig


class ProjectScanner(Protocol):
    def scan(self, project_path: Path, config: DiscoveryConfig) -> list[Path]:
        ...

    def file_hash(self, path: Path) -> str:
        ...
