from __future__ import annotations

from pathlib import Path
from typing import Protocol

from andocgen.config import OutputConfig
from andocgen.models.entities import DocBlock, ModuleModel, ProjectModel


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

    def update(self, cache_dir: Path, modules: list[ModuleModel]) -> None:
        ...


class PreviousDocLoader(Protocol):
    def extract(self, output_dir: Path, module_paths: list[str]) -> dict[str, str]:
        ...
