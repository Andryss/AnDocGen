from __future__ import annotations

import httpx

from andocgen.llm.base import ProviderRequestError, ProviderResponseError, ProviderTimeoutError
from andocgen.llm.schema import docblock_schema


class OllamaProvider:
    def __init__(self, base_url: str, model: str, timeout: float = 120.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def complete(self, system: str, user: str, *, entity_type: str = "function") -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "format": docblock_schema(entity_type),
        }
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as exc:
            raise ProviderTimeoutError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise ProviderRequestError(str(exc)) from exc
        except ValueError as exc:
            raise ProviderResponseError(str(exc)) from exc
        message = data.get("message", {})
        content = message.get("content", "") if isinstance(message, dict) else ""
        if not isinstance(content, str) or not content.strip():
            raise ProviderResponseError("Ollama provider returned empty content")
        return content.strip()
