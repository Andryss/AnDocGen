from __future__ import annotations

import re


def mostly_latin(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 25:
        return False
    if re.search(r"[а-яА-ЯёЁ]", stripped):
        return False
    letters = [char for char in stripped if char.isalpha()]
    if len(letters) < 12:
        return False
    latin = sum(1 for char in letters if ord(char) < 128)
    return latin / len(letters) > 0.5
