from __future__ import annotations

import ast

from andocgen.python.ast_utils import call_name, parse_python_calls, raised_exception_names, safe_unparse


def test_call_name_and_safe_unparse_handle_common_ast_nodes() -> None:
    expression = ast.parse("client.session.get(url)", mode="eval").body
    assert isinstance(expression, ast.Call)
    assert call_name(expression.func) == "client.session.get"
    assert safe_unparse(expression.args[0]) == "url"


def test_parse_python_calls_preserves_counts_and_keyword_names() -> None:
    calls = parse_python_calls("build(1, name='x')\nclient.run(force=True)")

    assert [(call.name, call.positional_count, call.keywords) for call in calls] == [
        ("build", 1, ["name"]),
        ("client.run", 0, ["force"]),
    ]


def test_raised_exception_names_extracts_direct_and_called_exceptions() -> None:
    assert raised_exception_names("raise ValueError('bad')\nraise RuntimeError") == {
        "RuntimeError",
        "ValueError",
    }
