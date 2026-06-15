from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from andocgen.config import OutputConfig
from andocgen.generator.formatter import format_markdown
from andocgen.models.entities import DocBlock, ModuleModel, ProjectModel


class MarkdownDocumentationWriter:
    def write(
        self,
        project: ProjectModel,
        blocks: list[DocBlock],
        config: OutputConfig,
        output_root: Path | None = None,
        all_module_paths: list[str] | None = None,
        language: str = "ru",
    ) -> list[str]:
        out_dir = Path(output_root or config.directory)
        out_dir.mkdir(parents=True, exist_ok=True)

        blocks_by_module: dict[str, list[DocBlock]] = defaultdict(list)
        for block in blocks:
            blocks_by_module[block.module_path].append(block)

        written: list[str] = []
        for module in project.modules:
            module_blocks = blocks_by_module.get(module.path, [])
            if not module_blocks:
                continue

            md_path = out_dir / f"{module.path}.md"
            md_path.parent.mkdir(parents=True, exist_ok=True)
            md_path.write_text(
                self._render_module_doc(project.name, module, module_blocks, language),
                encoding="utf-8",
            )
            written.append(str(md_path))

        readme_path = out_dir / "README.md"
        module_paths = all_module_paths or [m.path for m in project.modules]
        readme_path.write_text(
            self.render_project_readme(project, module_paths),
            encoding="utf-8",
        )
        written.append(str(readme_path))

        return written

    def render_project_readme(
        self,
        project: ProjectModel,
        module_paths: list[str],
        out_dir: Path | None = None,
    ) -> str:
        lines = [
            f"# {project.name}",
            "",
            project.project_description or "Документация проекта, сгенерированная AnDocGen.",
            "",
            "## Модули",
            "",
        ]
        for path in sorted(module_paths):
            lines.append(f"- [{path}]({path}.md)")
        lines.append("")
        return "\n".join(lines)

    def _render_module_doc(
        self,
        project_name: str,
        module: ModuleModel,
        blocks: list[DocBlock],
        language: str,
    ) -> str:
        module_block = next((b for b in blocks if b.entity_type == "module"), None)
        class_blocks = [b for b in blocks if b.entity_type == "class"]
        method_blocks = [b for b in blocks if b.entity_type == "method"]
        function_blocks = [b for b in blocks if b.entity_type == "function"]

        methods_by_class: dict[str, list[DocBlock]] = defaultdict(list)
        for method in method_blocks:
            class_name = method.entity_name.split(".", 1)[0]
            methods_by_class[class_name].append(method)

        lines = [
            f"# {project_name}",
            "",
            f"## Модуль `{module.path}`",
            "",
        ]

        if module_block:
            lines.extend(format_markdown(module_block, language, heading_level=2).splitlines())
            lines.append("")

        toc: list[str] = []
        if class_blocks:
            toc.append("- [Классы](#классы)")
        if function_blocks:
            toc.append("- [Функции](#функции)")
        if toc:
            lines.extend(["**Содержание:**", "", *toc, ""])

        if class_blocks:
            lines.extend(["## Классы", ""])
            for cls in class_blocks:
                lines.append(format_markdown(cls, language, heading_level=3))
                lines.append("")

                class_methods = methods_by_class.get(cls.entity_name, [])
                if class_methods:
                    lines.extend(["#### Методы", ""])
                    for method in class_methods:
                        lines.append(format_markdown(method, language, heading_level=5))
                        lines.append("")

        if function_blocks:
            lines.extend(["## Функции", ""])
            for fn in function_blocks:
                lines.append(format_markdown(fn, language, heading_level=3))
                lines.append("")

        return "\n".join(lines).rstrip() + "\n"
