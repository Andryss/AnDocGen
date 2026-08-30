from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from andocgen.llm.base import ProviderConfigError, ProviderRequestError, ProviderResponseError
from andocgen.llm.providers.openai_provider import OpenAIProvider
from andocgen.llm.schema import docblock_schema


def _make_provider(**kwargs: object) -> OpenAIProvider:
    defaults = {
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
        "model": "gpt-4o-mini",
    }
    defaults.update(kwargs)
    return OpenAIProvider(**defaults)  # type: ignore[arg-type]


@patch("andocgen.llm.providers.openai_provider.OpenAI")
def test_complete_returns_trimmed_content(mock_openai_cls: MagicMock) -> None:
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="  doc text  "))]
    )

    provider = _make_provider()
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}):
        result = provider.complete("sys", "user", entity_type="function")

    assert result == "doc text"
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "user"},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "andocgen_docblock",
                "strict": True,
                "schema": docblock_schema("function"),
            },
        },
    )


@patch("andocgen.llm.providers.openai_provider.OpenAI")
def test_complete_empty_choices(mock_openai_cls: MagicMock) -> None:
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(choices=[])

    provider = _make_provider()
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}):
        assert provider.complete("sys", "user", entity_type="function") == ""


def test_complete_missing_api_key_raises() -> None:
    provider = _make_provider()
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ProviderConfigError, match="OPENAI_API_KEY"):
            provider.complete("sys", "user", entity_type="function")


@patch("andocgen.llm.providers.openai_provider.OpenAI")
def test_complete_wraps_provider_request_errors(mock_openai_cls: MagicMock) -> None:
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.side_effect = RuntimeError("rate limit")

    provider = _make_provider()
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}):
        with pytest.raises(ProviderRequestError, match="rate limit"):
            provider.complete("sys", "user", entity_type="function")


@patch("andocgen.llm.providers.openai_provider.OpenAI")
def test_complete_rejects_malformed_provider_response(mock_openai_cls: MagicMock) -> None:
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content=None))])

    provider = _make_provider()
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}):
        with pytest.raises(ProviderResponseError, match="empty content"):
            provider.complete("sys", "user", entity_type="function")


@patch("andocgen.llm.providers.openai_provider.OpenAI")
def test_yandex_project_passed_to_client(mock_openai_cls: MagicMock) -> None:
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="ok"))]
    )

    provider = _make_provider(
        base_url="https://ai.api.cloud.yandex.net/v1",
        api_key_env="YANDEX_API_KEY",
        model="gpt://b1gtest/yandexgpt/latest",
        project="b1gtest",
        temperature=0.3,
        max_tokens=4000,
    )

    with patch.dict(os.environ, {"YANDEX_API_KEY": "AQVN-test"}):
        provider.complete("sys", "user", entity_type="function")

    mock_openai_cls.assert_called_once_with(
        api_key="AQVN-test",
        base_url="https://ai.api.cloud.yandex.net/v1",
        timeout=120.0,
        project="b1gtest",
    )
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt://b1gtest/yandexgpt/latest",
        messages=[
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "user"},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "andocgen_docblock",
                "strict": True,
                "schema": docblock_schema("function"),
            },
        },
        temperature=0.3,
        max_tokens=4000,
    )


@patch("andocgen.llm.providers.openai_provider.OpenAI")
def test_complete_uses_explicit_class_schema(mock_openai_cls: MagicMock) -> None:
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"summary":"ok"}'))]
    )

    provider = _make_provider()
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}):
        provider.complete("function-looking system prompt", "user", entity_type="class")

    kwargs = mock_client.chat.completions.create.call_args.kwargs
    schema = kwargs["response_format"]["json_schema"]["schema"]
    assert schema == docblock_schema("class")


def test_function_schema_uses_typed_examples() -> None:
    schema = docblock_schema("function")
    examples = schema["properties"]["examples"]

    assert examples["type"] == "array"
    item = examples["items"]
    assert item["required"] == ["description", "language", "code"]
    assert item["additionalProperties"] is False
