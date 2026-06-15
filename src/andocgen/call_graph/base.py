from __future__ import annotations

from typing import Protocol

from andocgen.models.entities import CallGraph, EntityContext, ProjectModel


class CallGraphBuilder(Protocol):
    def build(self, project: ProjectModel) -> CallGraph:
        ...

    def order_entities(self, contexts: list[EntityContext], graph: CallGraph) -> list[EntityContext]:
        ...

    def get_callee_ids(self, entity_id: str, graph: CallGraph) -> list[str]:
        ...

    def get_unresolved_calls(self, entity_id: str, graph: CallGraph) -> list[str]:
        ...
