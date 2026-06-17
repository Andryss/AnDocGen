from __future__ import annotations

import re

from andocgen.i18n.labels import LocaleLabels, get_labels
from andocgen.models.entities import DocBlock, ParameterDoc

_NA_PATTERN = re.compile(r"^N/A(?:\.|$|\s|-)", re.IGNORECASE)
_EMPTY_PHRASES = re.compile(
    r"^(?:"
    r"нет\s+(?:побочных\s+эффектов|исключений|граничных\s+случаев|примеров|полей)"
    r"|no\s+(?:side\s+effects|exceptions|edge\s+cases|examples|fields)"
    r"|none\.?"
    r")$",
    re.IGNORECASE,
)


def is_empty_section(text: str | None) -> bool:
    if text is None:
        return True
    stripped = text.strip()
    if not stripped:
        return True
    first_line = stripped.splitlines()[0].strip().strip("*`_ ")
    if _NA_PATTERN.match(first_line):
        return True
    return bool(_EMPTY_PHRASES.match(first_line))


def _sanitize_type(type_str: str) -> str:
    return type_str.replace("`", "").strip()


def format_markdown(block: DocBlock, language: str = "ru", heading_level: int = 3) -> str:
    labels = get_labels(language)
    if block.entity_type == "module":
        return _format_module(block, labels)
    if block.entity_type == "class":
        return _format_class(block, labels, heading_level)
    return _format_function(block, labels, heading_level)


def _heading(level: int, text: str) -> str:
    level = max(2, min(6, level))
    return f"{'#' * level} `{text}`"


def _display_signature(block: DocBlock) -> str:
    sig = block.signature or block.entity_name
    if block.entity_type == "method" and sig.startswith("def "):
        sig = sig[4:]
    if block.entity_type == "class" and not sig.startswith("class "):
        sig = f"class {sig}"
    return sig.strip()


def _render_prose(text: str) -> list[str]:
    body = text.strip()
    if not body:
        return []
    return ["", body, ""]


def _render_labeled_section(label: str, body: str) -> list[str]:
    if is_empty_section(body):
        return []
    return [f"**{label}:**", *_render_prose(body)]


def _format_function(block: DocBlock, labels: LocaleLabels, heading_level: int) -> str:
    lines = [_heading(heading_level, _display_signature(block)), *_render_prose(block.summary)]

    if block.parameters:
        lines.append(f"**{labels.parameters}:**")
        lines.append("")
        for param in block.parameters:
            type_part = f" (`{_sanitize_type(param.type)}`)" if param.type else ""
            desc = param.description or "—"
            lines.append(f"- `{param.name}`{type_part} — {desc}")
        lines.append("")

    if block.returns and (block.returns.type or block.returns.description):
        lines.append(f"**{labels.returns}:**")
        lines.append("")
        ret_type = block.returns.type
        ret_desc = block.returns.description or "—"
        if ret_type:
            lines.append(f"- `{_sanitize_type(ret_type)}` — {ret_desc}")
        else:
            lines.append(ret_desc)
        lines.append("")

    for key, value in [
        ("raises", block.raises),
        ("edge_cases", block.edge_cases),
        ("side_effects", block.side_effects),
        ("examples", block.examples),
        ("see_also", block.see_also),
    ]:
        lines.extend(_render_labeled_section(getattr(labels, key), value or ""))

    return "\n".join(lines).rstrip()


def _format_class(block: DocBlock, labels: LocaleLabels, heading_level: int) -> str:
    lines = [_heading(heading_level, _display_signature(block)), *_render_prose(block.summary)]

    if block.fields:
        lines.append(f"**{labels.fields}:**")
        lines.append("")
        for field in block.fields:
            type_part = f" (`{_sanitize_type(field.type)}`)" if field.type else ""
            lines.append(f"- `{field.name}`{type_part} — {field.description or '—'}")
        lines.append("")

    inheritance = block.inheritance or ""
    if inheritance and not _is_noise_inheritance(inheritance):
        lines.extend(_render_labeled_section(labels.inheritance, inheritance))

    return "\n".join(lines).rstrip()


def _is_noise_inheritance(text: str) -> bool:
    stripped = text.strip().strip("`- ")
    return stripped.lower() in ("object", "object —", "- object")


def _format_module(block: DocBlock, labels: LocaleLabels) -> str:
    lines = list(_render_prose(block.summary))
    if block.exports:
        lines.append(f"**{labels.exports}:**")
        lines.append("")
        for export in block.exports:
            type_part = f" (`{_sanitize_type(export.type)}`)" if export.type else ""
            lines.append(f"- `{export.name}`{type_part} — {export.description or '—'}")
        lines.append("")
    return "\n".join(lines).rstrip()
