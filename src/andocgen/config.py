from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ProjectConfig:
    name: str = ""
    description: str = ""


@dataclass
class DiscoveryConfig:
    implementation: str = "filesystem"
    extensions: list[str] = field(default_factory=lambda: [".py"])
    exclude_dirs: list[str] = field(
        default_factory=lambda: [
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            ".cache",
            "generated_docs",
            "node_modules",
        ]
    )


@dataclass
class ExtractionConfig:
    implementation: str = ""
    language: str = "python"

    def resolved_implementation(self) -> str:
        if self.implementation:
            return self.implementation
        if self.language == "python":
            return "python_ast"
        return self.language


@dataclass
class CallGraphConfig:
    implementation: str = "static"


@dataclass
class ContextConfig:
    implementation: str = "default"
    prompt: str = "sectioned"
    include_source_body: bool = True
    include_imports: bool = True
    include_call_graph: bool = True
    readme_limit: int = 2000
    max_context_chars: int = 32000


@dataclass
class OllamaProviderConfig:
    base_url: str = "http://localhost:11434"
    model: str = "llama3"


@dataclass
class OpenAIProviderConfig:
    base_url: str = "https://api.openai.com/v1"
    api_key_env: str = "OPENAI_API_KEY"
    model: str = "gpt-4o-mini"


@dataclass
class GenerationConfig:
    implementation: str = "llm"
    provider: str = "mock"
    language: str = "ru"
    incremental: bool = True
    providers: dict[str, Any] = field(default_factory=dict)

    @property
    def ollama(self) -> OllamaProviderConfig:
        return _merge_dataclass(OllamaProviderConfig, self.providers.get("ollama"))

    @property
    def openai(self) -> OpenAIProviderConfig:
        return _merge_dataclass(OpenAIProviderConfig, self.providers.get("openai"))


@dataclass
class ValidationConfig:
    implementation: str = "structured"
    check_completeness: bool = True
    check_consistency: bool = True
    check_structure: bool = True
    check_representation: bool = True
    check_text_quality: bool = True
    complexity_warning_threshold: int = 20
    min_summary_length: int = 10


@dataclass
class OutputConfig:
    implementation: str = "markdown"
    directory: str = "./generated_docs"
    format: str = "markdown"
    cache_path: str = ""


@dataclass
class ReportingConfig:
    implementation: str = "file"
    logs_dir: str = ""
    summary_file: str = "summary.txt"
    detail_file: str = "detail.json"
    trace_file: str = "trace.log"
    log_llm_content: bool = True
    trace_max_chars: int = 12000


@dataclass
class AppConfig:
    project: ProjectConfig = field(default_factory=ProjectConfig)
    discovery: DiscoveryConfig = field(default_factory=DiscoveryConfig)
    extraction: ExtractionConfig = field(default_factory=ExtractionConfig)
    call_graph: CallGraphConfig = field(default_factory=CallGraphConfig)
    context: ContextConfig = field(default_factory=ContextConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    reporting: ReportingConfig = field(default_factory=ReportingConfig)

    def resolve_output_dir(self) -> Path:
        return Path(self.output.directory)

    def resolve_cache_dir(self) -> Path:
        if self.output.cache_path:
            return Path(self.output.cache_path)
        return self.resolve_output_dir() / ".cache"

    def resolve_logs_dir(self) -> Path:
        if self.reporting.logs_dir:
            return Path(self.reporting.logs_dir)
        return self.resolve_output_dir() / "logs"


def _merge_dataclass(cls: type, data: dict[str, Any] | None) -> Any:
    if not data:
        return cls()
    fields = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
    filtered = {k: v for k, v in data.items() if k in fields}
    return cls(**filtered)


def load_config(path: Path | None = None) -> AppConfig:
    if path is None or not path.exists():
        return AppConfig()

    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    return AppConfig(
        project=_merge_dataclass(ProjectConfig, raw.get("project")),
        discovery=_merge_dataclass(DiscoveryConfig, raw.get("discovery")),
        extraction=_merge_dataclass(ExtractionConfig, raw.get("extraction")),
        call_graph=_merge_dataclass(CallGraphConfig, raw.get("call_graph")),
        context=_merge_dataclass(ContextConfig, raw.get("context")),
        generation=_merge_dataclass(GenerationConfig, raw.get("generation")),
        validation=_merge_dataclass(ValidationConfig, raw.get("validation")),
        output=_merge_dataclass(OutputConfig, raw.get("output")),
        reporting=_merge_dataclass(ReportingConfig, raw.get("reporting")),
    )
