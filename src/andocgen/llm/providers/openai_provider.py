from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


class OpenAIProvider:
    def __init__(
        self,
        base_url: str,
        api_key_env: str,
        model: str,
        project: str = "",
        timeout: float = 120.0,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.model = model
        self.project = project
        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client: OpenAI | None = None

    def _build_client(self) -> OpenAI:
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Environment variable {self.api_key_env} is not set for OpenAI provider"
            )

        kwargs: dict[str, Any] = {
            "api_key": api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
        }
        if self.project:
            kwargs["project"] = self.project

        return OpenAI(**kwargs)

    def _get_client(self) -> OpenAI:
        if self._client is None:
            self._client = self._build_client()
        return self._client

    def complete(self, system: str, user: str) -> str:
        client = self._get_client()
        request_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        if self.temperature is not None:
            request_kwargs["temperature"] = self.temperature
        if self.max_tokens is not None:
            request_kwargs["max_tokens"] = self.max_tokens

        response = client.chat.completions.create(**request_kwargs)

        choices = response.choices
        if not choices:
            return ""
        content = choices[0].message.content
        return (content or "").strip()
