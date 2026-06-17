from __future__ import annotations

from collections import defaultdict
from pathlib import PurePosixPath

from andocgen.i18n.labels import LocaleLabels, get_labels
from andocgen.models.entities import DocBlock, ModuleModel, ProjectModel


def package_dirs(groups: dict[str, list[str]]) -> list[str]:
    return sorted(key for key in groups if key)


def group_by_directory(module_paths: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for path in module_paths:
        parent = PurePosixPath(path).parent.as_posix()
        key = "" if parent == "." else parent
        groups[key].append(path)
    return dict(groups)


def sort_modules(paths: list[str]) -> list[str]:
    def sort_key(path: str) -> tuple[int, str]:
        name = PurePosixPath(path).name
        return (0 if name == "__init__.py" else 1, name)

    return sorted(paths, key=sort_key)


def module_summary(blocks: list[DocBlock]) -> str:
    for block in blocks:
        if block.entity_type == "module":
            text = block.summary.strip()
            if text:
                return text.splitlines()[0].strip()
    return "—"


class NavigationWriter:
    def write_all_readmes(
        self,
        out_dir,
        project: ProjectModel,
        module_paths: list[str],
        summaries: dict[str, str],
        language: str = "ru",
    ) -> list[str]:
        written: list[str] = []
        groups = group_by_directory(module_paths)
        dirs = package_dirs(groups)

        root_path = out_dir / "README.md"
        root_path.write_text(
            self.render_project_readme(project, module_paths, summaries, language),
            encoding="utf-8",
        )
        written.append(str(root_path))

        for subdir in dirs:
            readme_path = out_dir / subdir / "README.md"
            readme_path.parent.mkdir(parents=True, exist_ok=True)
            readme_path.write_text(
                self.render_directory_readme(subdir, groups[subdir], project, summaries, language),
                encoding="utf-8",
            )
            written.append(str(readme_path))

        return written

    def render_project_readme(
        self,
        project: ProjectModel,
        module_paths: list[str],
        summaries: dict[str, str] | None = None,
        language: str = "ru",
    ) -> str:
        labels = get_labels(language)
        summaries = summaries or {}
        groups = group_by_directory(module_paths)
        dirs = package_dirs(groups)

        lines = [f"# {project.name}", ""]
        lines.extend(_project_description_lines(project, labels))
        lines.append("")

        root_modules = sort_modules(groups.get("", []))
        if root_modules:
            lines.extend([f"## {labels.root_modules}", ""])
            lines.extend(_module_table(root_modules, summaries, labels, directory=""))
            lines.append("")

        if dirs:
            lines.extend([f"## {labels.packages}", ""])
            lines.append(
                f"| {labels.package} | {labels.module_count} | {labels.description} |"
            )
            lines.append("|--------|-------------|--------------|")
            for subdir in dirs:
                modules = groups[subdir]
                pkg_name = PurePosixPath(subdir).name
                init_path = f"{subdir}/__init__.py"
                desc = summaries.get(init_path) or summaries.get(modules[0], "—")
                lines.append(
                    f"| [{pkg_name}/]({subdir}/README.md) | {len(modules)} | {desc} |"
                )
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    def render_directory_readme(
        self,
        directory: str,
        module_paths: list[str],
        project: ProjectModel,
        summaries: dict[str, str],
        language: str = "ru",
    ) -> str:
        labels = get_labels(language)
        pkg_name = PurePosixPath(directory).name
        sorted_paths = sort_modules(module_paths)

        lines = [
            f"# {pkg_name}",
            "",
            f"[{labels.back_to_project}](../README.md)",
            "",
            f"## {labels.modules}",
            "",
        ]
        lines.extend(_module_table(sorted_paths, summaries, labels, directory=directory))
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"


def _module_table(
    module_paths: list[str],
    summaries: dict[str, str],
    labels: LocaleLabels,
    directory: str,
) -> list[str]:
    lines = [
        f"| {labels.module} | {labels.description} |",
        "|--------|--------------|",
    ]
    for path in module_paths:
        name = PurePosixPath(path).name
        link = _module_doc_link(path, directory)
        desc = summaries.get(path, "—")
        lines.append(f"| [{name}]({link}) | {desc} |")
    return lines


def _module_doc_link(path: str, directory: str) -> str:
    if directory:
        return f"{PurePosixPath(path).name}.md"
    return f"{path}.md"


def _project_description_lines(project: ProjectModel, labels: LocaleLabels) -> list[str]:
    desc = (project.project_description or "").strip()
    if not desc:
        return [labels.default_description]
    if desc.casefold() == project.name.casefold():
        return []
    return [desc]
