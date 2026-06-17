from __future__ import annotations

from collections import defaultdict
from pathlib import Path, PurePosixPath

from andocgen.generator.formatter import format_markdown
from andocgen.i18n.labels import get_labels
from andocgen.models.entities import DocBlock, ModuleModel


class ModuleDocAssembler:
    def write_module(
        self,
        module: ModuleModel,
        blocks: list[DocBlock],
        md_path: Path,
        language: str = "ru",
    ) -> None:
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(
            self.render_module_doc(module, blocks, language),
            encoding="utf-8",
        )

    def render_module_doc(
        self,
        module: ModuleModel,
        blocks: list[DocBlock],
        language: str = "ru",
    ) -> str:
        labels = get_labels(language)
        module_block = next((b for b in blocks if b.entity_type == "module"), None)
        class_blocks = [b for b in blocks if b.entity_type == "class"]
        method_blocks = [b for b in blocks if b.entity_type == "method"]
        function_blocks = [b for b in blocks if b.entity_type == "function"]

        methods_by_class: dict[str, list[DocBlock]] = defaultdict(list)
        for method in method_blocks:
            class_name = method.entity_name.split(".", 1)[0]
            methods_by_class[class_name].append(method)

        lines = [f"# {labels.module} `{module.path}`", ""]

        if module_block:
            lines.extend(format_markdown(module_block, language, heading_level=2).splitlines())
            lines.append("")

        toc: list[str] = []
        if class_blocks:
            toc.append(f"- [{labels.classes}](#{labels.classes.lower()})")
        if function_blocks:
            toc.append(f"- [{labels.functions}](#{labels.functions.lower()})")
        if toc:
            lines.extend([f"**{labels.contents}:**", "", *toc, ""])

        if class_blocks:
            lines.extend([f"## {labels.classes}", ""])
            for cls in class_blocks:
                lines.append(format_markdown(cls, language, heading_level=3))
                lines.append("")

                class_methods = methods_by_class.get(cls.entity_name, [])
                if class_methods:
                    lines.extend([f"#### {labels.methods}", ""])
                    for method in class_methods:
                        lines.append(format_markdown(method, language, heading_level=5))
                        lines.append("")

        if function_blocks:
            lines.extend([f"## {labels.functions}", ""])
            for fn in function_blocks:
                lines.append(format_markdown(fn, language, heading_level=3))
                lines.append("")

        lines.extend(["", "---", "", _module_nav_footer(module.path, labels)])
        return "\n".join(lines).rstrip() + "\n"


def _module_nav_footer(module_path: str, labels) -> str:
    parts = PurePosixPath(module_path).parts
    if len(parts) == 1:
        return f"[{labels.back_to_index}](README.md)"
    pkg = parts[0]
    return (
        f"[{labels.back_to_package} {pkg}](README.md) | "
        f"[{labels.back_to_project}](../README.md)"
    )
