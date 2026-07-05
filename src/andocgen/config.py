from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ConfigDict

from andocgen.generated.config_models import (
    AndocgenConfiguration,
    CallGraphConfig,
    ContextConfig,
    DiscoveryConfig,
    OllamaProvider,
    OpenAIProvider,
    OutputConfig,
    ProjectConfig,
    ReportingConfig,
    ValidationConfig,
)
from andocgen.generated.config_models import (
    ExtractionConfig as _ExtractionConfig,
)
from andocgen.generated.config_models import (
    GenerationConfig as _GenerationConfig,
)

ANDOCGEN_DIR = ".andocgen"

OllamaProviderConfig = OllamaProvider
OpenAIProviderConfig = OpenAIProvider


class ExtractionConfig(_ExtractionConfig):
    def resolved_implementation(self) -> str:
        implementation = self.implementation
        if implementation not in (None, ""):
            return str(implementation)
        language = self.language
        if language in (None, "python"):
            return "python_ast"
        return str(language)


class GenerationConfig(_GenerationConfig):
    @property
    def ollama(self) -> OllamaProvider:
        if self.providers and self.providers.ollama is not None:
            return self.providers.ollama
        return OllamaProvider()

    @property
    def openai(self) -> OpenAIProvider:
        if self.providers and self.providers.openai is not None:
            return self.providers.openai
        return OpenAIProvider()


class AppConfig(AndocgenConfiguration):
    model_config = ConfigDict(extra="ignore")

    project: ProjectConfig = ProjectConfig()
    discovery: DiscoveryConfig = DiscoveryConfig()
    extraction: ExtractionConfig = ExtractionConfig()
    call_graph: CallGraphConfig = CallGraphConfig()
    context: ContextConfig = ContextConfig()
    generation: GenerationConfig = GenerationConfig()
    validation: ValidationConfig = ValidationConfig()
    output: OutputConfig = OutputConfig()
    reporting: ReportingConfig = ReportingConfig()

    def resolve_output_dir(self) -> Path:
        return Path(self.output.directory or "./generated_docs")

    def resolve_andocgen_dir(self) -> Path:
        return self.resolve_output_dir() / ANDOCGEN_DIR

    def resolve_cache_dir(self) -> Path:
        if self.output.cache_path:
            return Path(self.output.cache_path)
        return self.resolve_andocgen_dir() / "cache"

    def resolve_logs_dir(self) -> Path:
        if self.reporting.logs_dir:
            return Path(self.reporting.logs_dir)
        return self.resolve_andocgen_dir() / "logs"


def load_config(path: Path | None = None) -> AppConfig:
    if path is None or not path.exists():
        return AppConfig()

    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    return AppConfig.model_validate(raw)
