from __future__ import annotations

from andocgen.config import DiscoveryConfig
from andocgen.registry import create_registered
from andocgen.scanner.base import ProjectScanner
from andocgen.scanner.implementations.filesystem import FilesystemScanner

_SCANNERS: dict[str, type[ProjectScanner]] = {
    "filesystem": FilesystemScanner,
}


def create_scanner(config: DiscoveryConfig) -> ProjectScanner:
    return create_registered(_SCANNERS, config.implementation, "scanner")
