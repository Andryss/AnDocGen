from __future__ import annotations

from andocgen.models.entities import DocBlock, ProjectModel
from andocgen.output.implementations.markdown_writer import MarkdownDocumentationWriter
from andocgen.output.navigation_writer import group_by_directory, sort_modules

MINI_LIBRARY_PATHS = [
    "__init__.py",
    "cli.py",
    "config.py",
    "exceptions.py",
    "models.py",
    "services.py",
    "storage.py",
    "plugins/__init__.py",
    "plugins/base.py",
    "plugins/markdown.py",
    "utils/__init__.py",
    "utils/formatting.py",
]


def test_group_by_directory() -> None:
    groups = group_by_directory(MINI_LIBRARY_PATHS)
    assert set(groups.keys()) == {"", "plugins", "utils"}
    assert len(groups[""]) == 7
    assert len(groups["plugins"]) == 3
    assert len(groups["utils"]) == 2


def test_sort_modules_init_first() -> None:
    sorted_paths = sort_modules(["services.py", "__init__.py", "cli.py"])
    assert sorted_paths[0] == "__init__.py"
    assert sorted_paths[1:] == ["cli.py", "services.py"]


def test_render_project_readme_structure() -> None:
    writer = MarkdownDocumentationWriter()
    project = ProjectModel(
        project_path="/tmp",
        modules=[],
        project_name="mini_library",
        project_description="Small multi-module example for AnDocGen.",
    )
    summaries = {
        "__init__.py": "Мини-библиотека с публичным API.",
        "services.py": "Модуль бизнес-логики.",
        "plugins/__init__.py": "Пакет плагинов.",
        "utils/__init__.py": "Утилиты форматирования.",
    }
    text = writer.render_project_readme(
        project, MINI_LIBRARY_PATHS, summaries, language="ru"
    )

    assert text.count("# mini_library") == 1
    assert "Small multi-module example" in text
    assert "## Корневые модули" in text
    assert "## Пакеты" in text
    assert "[__init__.py](__init__.py.md)" in text
    assert "[plugins/](plugins/README.md)" in text
    assert "[utils/](utils/README.md)" in text
    assert "- [cli.py]" not in text


def test_render_directory_readme() -> None:
    writer = MarkdownDocumentationWriter()
    project = ProjectModel(
        project_path="/tmp",
        modules=[],
        project_name="mini_library",
        project_description="",
    )
    summaries = {
        "plugins/base.py": "Базовый класс плагинов.",
        "plugins/__init__.py": "Пакет плагинов.",
    }
    text = writer.render_directory_readme(
        "plugins",
        ["plugins/markdown.py", "plugins/base.py", "plugins/__init__.py"],
        project,
        summaries,
        language="ru",
    )

    assert text.startswith("# plugins\n")
    assert "[← К проекту](../README.md)" in text
    assert "## Модули" in text
    assert "[__init__.py](__init__.py.md)" in text
    assert text.index("[__init__.py]") < text.index("[base.py]")


def test_write_root_readme_not_overwritten(tmp_path) -> None:
    from andocgen.config import OutputConfig
    from andocgen.models.entities import ModuleModel

    writer = MarkdownDocumentationWriter()
    project = ProjectModel(
        project_path="/tmp",
        modules=[
            ModuleModel(path="services.py"),
            ModuleModel(path="plugins/base.py"),
        ],
        project_name="mini_library",
        project_description="Small multi-module example.",
    )
    blocks = [
        DocBlock(
            entity_type="module",
            entity_name="services.py",
            module_path="services.py",
            signature="",
            summary="Business logic.",
            content="",
        ),
        DocBlock(
            entity_type="module",
            entity_name="plugins/base.py",
            module_path="plugins/base.py",
            signature="",
            summary="Plugin base.",
            content="",
        ),
    ]

    writer.write(
        project,
        blocks,
        OutputConfig(directory=str(tmp_path)),
        all_module_paths=MINI_LIBRARY_PATHS,
        language="ru",
    )
    root = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "# mini_library" in root
    assert "## Корневые модули" in root
    assert "## Пакеты" in root
    assert "[plugins/](plugins/README.md)" in root
    assert "← К проекту" not in root


def test_write_emits_directory_readmes(tmp_path) -> None:
    writer = MarkdownDocumentationWriter()
    project = ProjectModel(
        project_path="/tmp",
        modules=[],
        project_name="mini_library",
        project_description="Example project.",
    )
    blocks = [
        DocBlock(
            entity_type="module",
            entity_name="services.py",
            module_path="services.py",
            signature="",
            summary="Business logic module.",
            content="",
        )
    ]
    from andocgen.config import OutputConfig

    written = writer.write(
        project,
        blocks,
        OutputConfig(directory=str(tmp_path)),
        all_module_paths=["services.py", "plugins/base.py"],
        language="ru",
    )

    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "plugins" / "README.md").exists()
    assert str(tmp_path / "README.md") in written
    assert str(tmp_path / "plugins" / "README.md") in written
