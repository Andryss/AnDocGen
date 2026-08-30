from __future__ import annotations

import json

import httpx
import pytest

from andocgen.llm.providers.ollama import OllamaProvider
from andocgen.llm.schema import docblock_schema


def test_ollama_sends_structured_format(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}
    original_client = httpx.Client

    def handler(request: httpx.Request) -> httpx.Response:
        captured["payload"] = request.read()
        return httpx.Response(200, json={"message": {"content": '{"summary":"ok"}'}})

    def client_factory(*, timeout: float) -> httpx.Client:
        captured["timeout"] = timeout
        return original_client(transport=httpx.MockTransport(handler))

    monkeypatch.setattr(httpx, "Client", client_factory)
    provider = OllamaProvider("http://localhost:11434", "qwen2.5-coder:7b")

    assert provider.complete("sys", "user", entity_type="class") == '{"summary":"ok"}'

    payload = json.loads(captured["payload"])
    assert payload["format"] == docblock_schema("class")
