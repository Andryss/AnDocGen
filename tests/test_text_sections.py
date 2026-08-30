from __future__ import annotations

from andocgen.text.sections import is_empty_section


def test_is_empty_section_detects_na_and_empty_phrases() -> None:
    assert is_empty_section(None)
    assert is_empty_section("")
    assert is_empty_section("  **N/A**  ")
    assert is_empty_section("N/A\nextra explanation")
    assert is_empty_section("Нет побочных эффектов")
    assert is_empty_section("No side effects")
    assert not is_empty_section("ValueError on invalid input")
