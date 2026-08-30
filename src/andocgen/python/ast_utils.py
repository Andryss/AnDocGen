from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class PythonCall:
    name: str
    positional_count: int
    keywords: list[str]


def safe_unparse(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return type(node).__name__


def call_name(node: ast.expr, *, dotted: bool = True) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        if not dotted:
            return node.attr
        value = call_name(node.value, dotted=True) if not isinstance(node.value, ast.Name) else node.value.id
        if value:
            return f"{value}.{node.attr}"
        return node.attr
    return ""


def parse_python_calls(source: str, *, dotted: bool = True) -> list[PythonCall]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    calls: list[PythonCall] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = call_name(node.func, dotted=dotted)
        if not name:
            continue
        calls.append(
            PythonCall(
                name=name,
                positional_count=len(node.args),
                keywords=[kw.arg for kw in node.keywords if kw.arg],
            )
        )
    return calls


def raised_exception_names(source: str) -> set[str]:
    if not source.strip():
        return set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Raise) or node.exc is None:
            continue
        exc = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
        name = call_name(exc, dotted=False) if isinstance(exc, ast.expr) else ""
        if name:
            names.add(name)
    return names
