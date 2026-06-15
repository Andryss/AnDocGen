from __future__ import annotations

from pathlib import Path

from andocgen.context.base import ProjectMetadataLoader


class DefaultProjectMetadataLoader:
    def load_readme_excerpt(self, project_path: Path, limit: int) -> str | None:
        for name in ("README.md", "readme.md", "README.rst"):
            readme = project_path / name
            if readme.exists():
                text = readme.read_text(encoding="utf-8")
                return text[:limit]
        return None

    def load_project_description(self, project_path: Path, config_description: str) -> str:
        if config_description:
            return config_description
        readme = self.load_readme_excerpt(project_path, 500)
        if readme:
            return readme.splitlines()[0] if readme else ""
        pyproject = project_path / "pyproject.toml"
        if pyproject.exists():
            for line in pyproject.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("description"):
                    return line.split("=", 1)[-1].strip().strip('"').strip("'")
        return ""
