from __future__ import annotations

from pathlib import Path
from typing import Protocol

from andocgen.config import ContextConfig
from andocgen.context.doc_brief_registry import DocBriefRegistry
from andocgen.models.entities import CallGraph, EntityContext, ProjectModel


class ContextBuilder(Protocol):
    def build(
        self,
        project: ProjectModel,
        config: ContextConfig,
        output_language: str = "ru",
        readme_excerpt: str | None = None,
        previous_docs: dict[str, str] | None = None,
    ) -> list[EntityContext]:
        ...

    def attach_callee_docs(
        self,
        ctx: EntityContext,
        docs_by_id: dict[str, str],
        callee_ids: list[str],
        unresolved: list[str],
    ) -> None:
        ...

    def attach_related_briefs(
        self,
        ctx: EntityContext,
        registry: DocBriefRegistry,
        callee_ids: list[str],
        unresolved: list[str],
        call_graph: CallGraph,
    ) -> None:
        ...


class PromptBuilder(Protocol):
    def build_system_message(self, output_language: str, entity_type: str) -> str:
        ...

    def build_user_message(self, ctx: EntityContext, max_chars: int) -> str:
        ...


class ProjectMetadataLoader(Protocol):
    def load_readme_excerpt(
        self, project_path: Path, limit: int, readme_path: str = ""
    ) -> str | None:
        ...

    def load_project_description(self, project_path: Path, config_description: str) -> str:
        ...
