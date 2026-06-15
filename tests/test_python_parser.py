from __future__ import annotations

from pathlib import Path

from andocgen.config import ExtractionConfig
from andocgen.parser.factory import create_parser


def test_parse_function_complexity_and_calls(tmp_path: Path) -> None:
    source = '''
def divide(a: float, b: float):
    if b == 0:
        return None
    return a / b
'''
    path = tmp_path / "calc.py"
    path.write_text(source, encoding="utf-8")
    parser = create_parser(ExtractionConfig())
    result = parser.parse(path, tmp_path)
    assert result.error is None
    assert result.module is not None
    fn = result.module.functions[0]
    assert fn.name == "divide"
    assert fn.complexity == 2
    assert fn.source_body


def test_parse_method_decorators(tmp_path: Path) -> None:
    source = '''
class C:
    @staticmethod
    def foo(x: int) -> int:
        return x
'''
    path = tmp_path / "m.py"
    path.write_text(source, encoding="utf-8")
    parser = create_parser(ExtractionConfig())
    result = parser.parse(path, tmp_path)
    assert result.module is not None
    method = result.module.classes[0].methods[0]
    assert "staticmethod" in method.decorators
    assert method.is_method


def test_parse_syntax_error(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("def broken(:\n", encoding="utf-8")
    parser = create_parser(ExtractionConfig())
    result = parser.parse(path, tmp_path)
    assert result.module is None
    assert result.error is not None
