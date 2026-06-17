"""Markdown export plugin."""

from __future__ import annotations

from typing import Any

from mini_library.plugins.base import PluginBase


class MarkdownExporter(PluginBase):
    """Export order summaries as Markdown."""

    def __init__(self, *args: Any, heading: str = "## Summary", **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.heading = heading

    def export(self, data: dict[str, Any]) -> str:
        lines = [self.heading, ""]
        for key, value in data.items():
            lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)
