from __future__ import annotations

from andocgen.config import DiscoveryConfig
from andocgen.scanner.base import ProjectScanner
from andocgen.scanner.implementations.filesystem import FilesystemScanner

_SCANNERS: dict[str, type] = {
    "filesystem": FilesystemScanner,
}


def create_scanner(config: DiscoveryConfig) -> ProjectScanner:
    impl = config.implementation.lower()
    if impl not in _SCANNERS:
        raise ValueError(f"Unknown scanner implementation: {config.implementation}")
    return _SCANNERS[impl]()
