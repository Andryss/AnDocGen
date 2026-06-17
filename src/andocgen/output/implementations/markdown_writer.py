from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from andocgen.config import OutputConfig
from andocgen.models.entities import DocBlock, ProjectModel
from andocgen.output.module_doc_assembler import ModuleDocAssembler
from andocgen.output.navigation_writer import NavigationWriter, module_summary


class MarkdownDocumentationWriter:
    def __init__(self) -> None:
        self._assembler = ModuleDocAssembler()
        self._navigation = NavigationWriter()

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
        documented_paths: list[str] = []
        for module in project.modules:
            module_blocks = blocks_by_module.get(module.path, [])
            if not module_blocks:
                continue

            documented_paths.append(module.path)
            md_path = out_dir / f"{module.path}.md"
            self._assembler.write_module(module, module_blocks, md_path, language)
            written.append(str(md_path))

        module_paths = all_module_paths or documented_paths
        summaries = {
            path: module_summary(blocks_by_module.get(path, []))
            for path in module_paths
            if path in blocks_by_module
        }
        written.extend(
            self._navigation.write_all_readmes(
                out_dir, project, module_paths, summaries, language
            )
        )

        return written

    def render_project_readme(
        self,
        project: ProjectModel,
        module_paths: list[str],
        summaries: dict[str, str] | None = None,
        language: str = "ru",
        out_dir: Path | None = None,
    ) -> str:
        return self._navigation.render_project_readme(
            project, module_paths, summaries, language
        )

    def render_directory_readme(
        self,
        directory: str,
        module_paths: list[str],
        project: ProjectModel,
        summaries: dict[str, str],
        language: str = "ru",
    ) -> str:
        return self._navigation.render_directory_readme(
            directory, module_paths, project, summaries, language
        )
