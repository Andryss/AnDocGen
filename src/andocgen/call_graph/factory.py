from __future__ import annotations

from andocgen.call_graph.base import CallGraphBuilder
from andocgen.call_graph.implementations.static import StaticCallGraphBuilder
from andocgen.config import CallGraphConfig

_BUILDERS: dict[str, type] = {
    "static": StaticCallGraphBuilder,
}


def create_call_graph_builder(config: CallGraphConfig) -> CallGraphBuilder:
    impl = config.implementation.lower()
    if impl not in _BUILDERS:
        raise ValueError(f"Unknown call graph implementation: {config.implementation}")
    return _BUILDERS[impl]()
