from __future__ import annotations

from andocgen.config import GenerationConfig
from andocgen.llm.base import LLMProvider
from andocgen.llm.providers.mock import MockProvider
from andocgen.llm.providers.ollama import OllamaProvider
from andocgen.llm.providers.openai_provider import OpenAIProvider

_PROVIDERS: dict[str, type] = {
    "mock": MockProvider,
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
}


def create_llm_provider(config: GenerationConfig) -> LLMProvider:
    provider = config.provider.lower()
    if provider not in _PROVIDERS:
        raise ValueError(f"Unknown LLM provider: {config.provider}")

    if provider == "mock":
        return MockProvider(language=config.language)
    if provider == "ollama":
        return OllamaProvider(
            base_url=config.ollama.base_url,
            model=config.ollama.model,
        )
    return OpenAIProvider(
        base_url=config.openai.base_url,
        api_key_env=config.openai.api_key_env,
        model=config.openai.model,
    )
