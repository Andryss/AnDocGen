from __future__ import annotations

from andocgen.output.implementations.markdown_previous_doc import MarkdownPreviousDocLoader


def test_previous_doc_loader_uses_english_section_headers() -> None:
    text = """# sample

## Module

Module summary text.

## Classes

### `class Foo`

Class summary.

## Functions

### `def bar()`

Function summary.
"""
    loader = MarkdownPreviousDocLoader()
    docs = loader._parse_module_doc(text, "sample.py", type("L", (), {
        "module": "Module",
        "classes": "Classes",
        "functions": "Functions",
    })())
    assert any("Module summary" in value for value in docs.values())
    assert any("Class summary" in value for value in docs.values())
    assert any("Function summary" in value for value in docs.values())
