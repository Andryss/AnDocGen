from __future__ import annotations

from andocgen.call_graph.base import CallGraphBuilder
from andocgen.call_graph.implementations.static import StaticCallGraphBuilder
from andocgen.config import CallGraphConfig
from andocgen.registry import create_registered

_BUILDERS: dict[str, type[CallGraphBuilder]] = {
    "static": StaticCallGraphBuilder,
}


def create_call_graph_builder(config: CallGraphConfig) -> CallGraphBuilder:
    return create_registered(_BUILDERS, config.implementation, "call graph")
