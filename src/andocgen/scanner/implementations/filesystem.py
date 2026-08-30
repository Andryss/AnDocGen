from __future__ import annotations

import hashlib
from pathlib import Path

from andocgen.config import DiscoveryConfig


class FilesystemScanner:
    def scan(self, project_path: Path, config: DiscoveryConfig) -> list[Path]:
        exclude = set(config.exclude_dirs or [])
        extensions = set(config.extensions or [])
        results: list[Path] = []

        for path in project_path.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in extensions:
                continue
            if any(part in exclude for part in path.parts):
                continue
            results.append(path)

        return sorted(results)

    def file_hash(self, path: Path) -> str:
        content = path.read_bytes()
        return hashlib.sha256(content).hexdigest()
