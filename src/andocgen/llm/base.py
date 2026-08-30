from __future__ import annotations

from typing import Protocol


class LLMProviderError(RuntimeError):
    pass


class ProviderConfigError(LLMProviderError):
    pass


class ProviderRequestError(LLMProviderError):
    pass


class ProviderTimeoutError(ProviderRequestError):
    pass


class ProviderResponseError(LLMProviderError):
    pass


class LLMProvider(Protocol):
    def complete(self, system: str, user: str, *, entity_type: str = "function") -> str:
        ...
