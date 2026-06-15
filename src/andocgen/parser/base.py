from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from andocgen.models.entities import ModuleModel


@dataclass
class ParseResult:
    module: ModuleModel | None = None
    error: str | None = None


class SourceParser(Protocol):
    def parse(self, file_path: Path, project_root: Path) -> ParseResult:
        ...
