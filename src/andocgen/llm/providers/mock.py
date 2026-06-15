from __future__ import annotations

import re


class MockProvider:
    """Deterministic section-format documentation for local testing."""

    def __init__(self, language: str = "ru") -> None:
        self.language = language

    def complete(self, system: str, user: str) -> str:
        ctx = _parse_user_message(user)
        if ctx["entity_type"] == "module":
            return _module_doc(ctx)
        if ctx["entity_type"] == "class":
            return _class_doc(ctx)
        return _function_doc(ctx)


def _parse_user_message(user: str) -> dict[str, str]:
    ctx: dict[str, str] = {
        "entity_type": "function",
        "entity_name": "unknown",
        "signature": "",
        "docstring": "",
    }
    entity_section = _extract_section(user, "Entity")
    if entity_section:
        for line in entity_section.splitlines():
            if line.startswith("Type:"):
                ctx["entity_type"] = line.split(":", 1)[1].strip()
            elif line.startswith("Name:"):
                ctx["entity_name"] = line.split(":", 1)[1].strip()
            elif line.startswith("Signature:"):
                ctx["signature"] = line.split(":", 1)[1].strip()

    source_section = _extract_section(user, "Source")
    if source_section:
        if "Docstring:" in source_section:
            ctx["docstring"] = source_section.split("Docstring:", 1)[1].split("Source body:", 1)[0].strip()
    return ctx


def _extract_section(text: str, title: str) -> str:
    marker = f"## {title}"
    if marker not in text:
        return ""
    start = text.index(marker) + len(marker)
    rest = text[start:].lstrip("\n")
    next_idx = rest.find("\n## ")
    return rest[:next_idx] if next_idx >= 0 else rest


def _module_doc(ctx: dict[str, str]) -> str:
    name = ctx["entity_name"]
    desc = ctx["docstring"] or f"Модуль `{name}`."
    return f"""## Summary

{desc}

## Exports

N/A
"""


def _class_doc(ctx: dict[str, str]) -> str:
    name = ctx["entity_name"]
    desc = ctx["docstring"] or f"Класс `{name}`."
    return f"""## Summary

{desc}

## Fields

N/A

## Inheritance

N/A

## Methods overview

N/A
"""


def _function_doc(ctx: dict[str, str]) -> str:
    name = ctx["entity_name"]
    sig = ctx["signature"]
    desc = ctx["docstring"] or f"Выполняет операцию `{name.split('.')[-1]}`."
    params = _parse_params_from_signature(sig)
    param_lines = "\n".join(
        f"- `{p['name']}` (`{p['type']}`) — параметр функции" for p in params
    ) or "N/A"
    ret_type = _parse_return_type(sig)
    ret_line = f"- `{ret_type}` — результат операции" if ret_type else "N/A"

    return f"""## Summary

{desc}

## Parameters

{param_lines}

## Returns

{ret_line}

## Raises

N/A

## Edge cases

N/A

## Side effects

N/A

## Examples

N/A

## See also

N/A
"""


def _parse_params_from_signature(signature: str) -> list[dict[str, str]]:
    if "(" not in signature or ")" not in signature:
        return []
    inner = signature[signature.index("(") + 1 : signature.rindex(")")]
    if not inner.strip():
        return []
    params: list[dict[str, str]] = []
    for part in _split_params(inner):
        part = part.strip()
        if not part or part in ("self", "cls"):
            continue
        if ": " in part:
            name, typ = part.split(": ", 1)
            name = name.split("=")[0].strip()
            typ = typ.split("=")[0].strip()
        else:
            name = part.split("=")[0].strip()
            typ = ""
        if name.startswith("*"):
            continue
        params.append({"name": name, "type": typ or "Any"})
    return params


def _split_params(inner: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in inner:
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        if char == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    if current:
        parts.append("".join(current))
    return parts


def _parse_return_type(signature: str) -> str:
    if "->" not in signature:
        return ""
    return signature.split("->", 1)[1].strip()
