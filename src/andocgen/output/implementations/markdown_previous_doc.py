from __future__ import annotations

import re
from pathlib import Path

from andocgen.i18n.labels import get_labels
from andocgen.models.entities import EntityType, make_entity_id


class MarkdownPreviousDocLoader:
    def extract(
        self,
        output_dir: Path,
        module_paths: list[str],
        language: str = "ru",
    ) -> dict[str, str]:
        docs: dict[str, str] = {}
        root = Path(output_dir)
        labels = get_labels(language)
        for module_path in module_paths:
            md_path = root / f"{module_path}.md"
            if not md_path.exists():
                continue
            text = md_path.read_text(encoding="utf-8")
            docs.update(self._parse_module_doc(text, module_path, labels))
        return docs

    def _parse_module_doc(self, text: str, module_path: str, labels) -> dict[str, str]:
        docs: dict[str, str] = {}
        module_id = make_entity_id(module_path, "module", module_path)
        module_header = f"## {labels.module}"
        classes_header = f"## {labels.classes}"
        functions_header = f"## {labels.functions}"
        module_body = _section_between(
            text,
            module_header,
            [classes_header, functions_header],
        )
        if module_body:
            docs[module_id] = module_body.strip()

        for section_title, entity_type in [
            (classes_header, "class"),
            (functions_header, "function"),
        ]:
            if section_title not in text:
                continue
            section = text.split(section_title, 1)[1]
            next_header = re.search(r"\n## ", section)
            if next_header:
                section = section[: next_header.start()]
            for block in re.split(r"(?=^### `)", section, flags=re.MULTILINE):
                block = block.strip()
                if not block.startswith("### `"):
                    continue
                header_match = re.match(r"^### `(.+?)`", block)
                if not header_match:
                    continue
                header = header_match.group(1)
                if entity_type == "class" and header.startswith("class "):
                    name = header.split("(")[0].replace("class ", "").strip()
                    entity_id = make_entity_id(module_path, "class", name)
                elif entity_type == "function":
                    name = header.split("(")[0].strip()
                    kind: EntityType = "method" if "." in name else "function"
                    entity_id = make_entity_id(module_path, kind, name)
                else:
                    continue
                docs[entity_id] = block
        return docs


def _section_between(text: str, start_header: str, end_headers: list[str]) -> str:
    if start_header not in text:
        return ""
    start = text.index(start_header)
    rest = text[start:]
    end_positions = [rest.find(h) for h in end_headers if h in rest]
    end_positions = [p for p in end_positions if p > 0]
    if end_positions:
        rest = rest[: min(end_positions)]
    lines = rest.splitlines()[1:]
    return "\n".join(lines)
