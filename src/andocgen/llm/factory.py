from __future__ import annotations

from collections.abc import Callable

from andocgen.config import GenerationConfig
from andocgen.llm.base import LLMProvider
from andocgen.llm.providers.mock import MockProvider
from andocgen.llm.providers.ollama import OllamaProvider
from andocgen.llm.providers.openai_provider import OpenAIProvider

_PROVIDERS = {"mock", "ollama", "openai"}


def create_llm_provider(config: GenerationConfig) -> LLMProvider:
    provider = str(config.provider or "mock").lower()
    if provider not in _PROVIDERS:
        raise ValueError(f"Unknown LLM provider: {config.provider}")

    if provider == "mock":
        return MockProvider(language=config.language or "ru")
    if provider == "ollama":
        ollama = config.ollama
        return OllamaProvider(
            base_url=ollama.base_url or "http://localhost:11434",
            model=ollama.model or "llama3",
            timeout=ollama.timeout or 120.0,
        )
    openai = config.openai
    return OpenAIProvider(
        base_url=openai.base_url or "https://api.openai.com/v1",
        api_key_env=openai.api_key_env or "OPENAI_API_KEY",
        model=openai.model or "gpt-4o-mini",
        project=openai.project or "",
        timeout=openai.timeout or 120.0,
        temperature=openai.temperature,
        max_tokens=openai.max_tokens,
    )


def create_llm_provider_factory(config: GenerationConfig) -> Callable[[], LLMProvider]:
    def factory() -> LLMProvider:
        return create_llm_provider(config)

    return factory
