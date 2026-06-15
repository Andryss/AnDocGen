from __future__ import annotations

from andocgen.config import ExtractionConfig
from andocgen.parser.base import SourceParser
from andocgen.parser.implementations.python_ast import PythonAstParser

_PARSERS: dict[str, type] = {
    "python_ast": PythonAstParser,
}


def create_parser(config: ExtractionConfig) -> SourceParser:
    impl = config.resolved_implementation().lower()
    if impl not in _PARSERS:
        raise ValueError(f"Unknown parser implementation: {impl}")
    return _PARSERS[impl]()
