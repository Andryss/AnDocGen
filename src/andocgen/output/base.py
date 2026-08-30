from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Protocol

from andocgen.config import OutputConfig
from andocgen.models.entities import CallGraph, DocBlock, ModuleModel, ProjectModel

if TYPE_CHECKING:
    from andocgen.generation_plan import CacheSnapshot


class DocumentationWriter(Protocol):
    def write(
        self,
        project: ProjectModel,
        blocks: list[DocBlock],
        config: OutputConfig,
        output_root: Path | None = None,
        all_module_paths: list[str] | None = None,
        language: str = "ru",
    ) -> list[str]:
        ...

    def render_project_readme(
        self,
        project: ProjectModel,
        module_paths: list[str],
        summaries: dict[str, str] | None = None,
        language: str = "ru",
        out_dir: Path | None = None,
    ) -> str:
        ...


class CacheStore(Protocol):
    def load(self, cache_dir: Path) -> dict[str, str]:
        ...

    def load_snapshot(self, cache_dir: Path) -> CacheSnapshot:
        ...

    def update(
        self,
        cache_dir: Path,
        modules: list[ModuleModel],
        blocks: list[DocBlock] | None = None,
        graph: CallGraph | None = None,
    ) -> None:
        ...


class PreviousDocLoader(Protocol):
    def extract(
        self,
        output_dir: Path,
        module_paths: list[str],
        language: str = "ru",
    ) -> dict[str, str]:
        ...
