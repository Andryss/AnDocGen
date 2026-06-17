from __future__ import annotations

import re


def normalize_llm_response(raw: str) -> str:
    text = raw.strip()
    fence = re.match(r"^```(?:markdown|md|json)?\s*\n(.*)\n```\s*$", text, re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    if text.startswith("{") and "## Summary" not in text:
        return text
    return text
