from __future__ import annotations

import re

from andocgen.generator.formatter import is_empty_section
from andocgen.models.entities import (
    DocBlock,
    EntityContext,
    EntityType,
    ExportDoc,
    ParameterDoc,
    ReturnDoc,
)


class SectionParseError(Exception):
    pass


_FUNCTION_SECTIONS = [
    "Summary",
    "Parameters",
    "Returns",
    "Raises",
    "Edge cases",
    "Side effects",
    "Examples",
    "See also",
]
_CLASS_SECTIONS = ["Summary", "Fields", "Inheritance", "Methods overview"]
_MODULE_SECTIONS = ["Summary", "Exports"]


def parse_sections(raw_response: str, ctx: EntityContext) -> DocBlock:
    from andocgen.generator.response_sanitizer import normalize_llm_response

    raw_response = normalize_llm_response(raw_response)
    sections = _split_sections(raw_response)
    required = _required_sections(ctx.entity_type)
    missing = [s for s in required if s not in sections]
    if missing:
        raise SectionParseError(f"Missing required sections: {', '.join(missing)}")

    block = DocBlock(
        entity_type=ctx.entity_type,
        entity_name=ctx.entity_name,
        module_path=ctx.module_path,
        signature=ctx.signature,
        raw_response=raw_response.strip(),
        summary=sections["Summary"].strip(),
    )

    if ctx.entity_type in ("function", "method"):
        block.parameters = _parse_parameters(sections["Parameters"])
        block.returns = _parse_returns(sections["Returns"])
        block.raises = _normalize_optional_section(sections["Raises"])
        block.edge_cases = _normalize_optional_section(sections["Edge cases"])
        block.side_effects = _normalize_optional_section(sections["Side effects"])
        block.examples = _normalize_optional_section(sections["Examples"])
        block.see_also = _normalize_optional_section(sections["See also"])
    elif ctx.entity_type == "class":
        block.fields = _parse_parameters(sections.get("Fields", "N/A"))
        block.inheritance = sections.get("Inheritance", "N/A").strip()
        block.methods_overview = _normalize_optional_section(sections.get("Methods overview", "N/A"))
    elif ctx.entity_type == "module":
        block.exports = _parse_exports(sections["Exports"])

    return block


def _required_sections(entity_type: EntityType) -> list[str]:
    if entity_type in ("function", "method"):
        return _FUNCTION_SECTIONS
    if entity_type == "class":
        return ["Summary"]
    return _MODULE_SECTIONS


def _split_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[title] = text[start:end].strip()
    return sections


def _normalize_optional_section(section: str) -> str:
    text = section.strip()
    if is_empty_section(text):
        return "N/A"
    return text


def _parse_parameters(section: str) -> list[ParameterDoc]:
    if is_empty_section(section):
        return []
    params: list[ParameterDoc] = []
    seen: set[str] = set()
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        parsed = _parse_parameter_line(line)
        if parsed and parsed.name not in seen:
            params.append(parsed)
            seen.add(parsed.name)
    return params


def _parse_parameter_line(line: str) -> ParameterDoc | None:
    patterns = [
        r"-\s+`([^`]+)`\s+\(`([^`]*)`\)\s+[-—–]\s*(.+)$",
        r"-\s+`([^`]+)`\s+[-—–]\s*(.+)$",
        r"-\s+\*\*([^*]+)\*\*:\s*\(([^)]+)\)\s+(.+)$",
        r"-\s+\*\*([^*]+)\*\*:\s*\(([^)]+)\)\s*[-—–]\s*(.+)$",
        r"-\s+\*\*([^*]+)\*\*\s*\(([^)]+)\)\s*:\s*(.+)$",
        r"-\s+\*\*([^*]+)\*\*:\s*(.+)$",
        r"-\s+`?(\w+)`?\s+\(([^)]+)\)\s*:\s*(.+)$",
        r"-\s+`?(\w+)`?\s+\(([^)]+)\)\s+[-—–]\s*(.+)$",
        r"-\s+`?(\w+)`?\s*:\s*\(([^)]+)\)\s*(.+)$",
    ]
    for pattern in patterns:
        match = re.match(pattern, line)
        if not match:
            continue
        groups = match.groups()
        if len(groups) == 3:
            name, typ, desc = groups
            return ParameterDoc(name=name.strip(), type=typ.strip(), description=desc.strip())
        if len(groups) == 2:
            name, desc = groups
            return ParameterDoc(name=name.strip(), type="", description=desc.strip())
    return None


def _parse_returns(section: str) -> ReturnDoc | None:
    if is_empty_section(section):
        return None
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        for pattern in (
            r"-\s+`([^`]+)`\s+[-—–]\s*(.+)$",
            r"-\s+\*\*([^*]+)\*\*:\s*(.+)$",
            r"-\s+`?(\w+)`?\s*:\s*(.+)$",
        ):
            match = re.match(pattern, line)
            if match:
                return ReturnDoc(type=match.group(1).strip(), description=match.group(2).strip())
    text = section.strip().lstrip("- ").strip()
    if text.upper().startswith("RETURNS"):
        text = text.split(":", 1)[-1].strip()
    if text:
        type_match = re.match(r"^`?(\w[\w\[\], ]*)`?\s*[-—–:]?\s*(.*)$", text)
        if type_match and type_match.group(2):
            return ReturnDoc(type=type_match.group(1).strip(), description=type_match.group(2).strip())
        return ReturnDoc(type="", description=text)
    return None


def _parse_exports(section: str) -> list[ExportDoc]:
    if is_empty_section(section):
        return []
    exports: list[ExportDoc] = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        match = re.match(r"-\s+`([^`]+)`(?:\s+\(`([^`]*)`\))?\s+[-—–]\s*(.+)$", line)
        if match:
            exports.append(
                ExportDoc(
                    name=match.group(1),
                    type=match.group(2) or None,
                    description=match.group(3).strip(),
                )
            )
    return exports
