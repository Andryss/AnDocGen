from __future__ import annotations

import re

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
