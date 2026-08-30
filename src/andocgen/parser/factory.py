from __future__ import annotations

from andocgen.config import ExtractionConfig
from andocgen.parser.base import SourceParser
from andocgen.parser.implementations.python_ast import PythonAstParser
from andocgen.registry import create_registered

_PARSERS: dict[str, type[SourceParser]] = {
    "python_ast": PythonAstParser,
}


def create_parser(config: ExtractionConfig) -> SourceParser:
    return create_registered(_PARSERS, config.resolved_implementation(), "parser")
