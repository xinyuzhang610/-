import asyncio

import httpx
import pytest

from config import Settings
from services.deepseek import DeepSeekRequestError, chat_with_deepseek


class FakeAsyncClient:
    def __init__(self, response=None, exception=None):
        self.response = response
        self.exception = exception

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return False

    async def post(self, *args, **kwargs):
        if self.exception:
            raise self.exception
        return self.response


def configure_live_provider(monkeypatch):
    monkeypatch.setattr(
        "services.deepseek.settings",
        Settings(AI_PROVIDER="deepseek", DEEPSEEK_API_KEY="test-key", DEEPSEEK_MODEL="deepseek-v4-flash"),
    )


def test_invalid_model_response_is_a_safe_configuration_error(monkeypatch):
    configure_live_provider(monkeypatch)
    response = httpx.Response(
        400,
        json={"error": {"message": "unsupported model dsv4", "type": "invalid_request_error"}},
        request=httpx.Request("POST", "https://api.deepseek.com/v1/chat/completions"),
    )
    monkeypatch.setattr("services.deepseek.httpx.AsyncClient", lambda: FakeAsyncClient(response=response))

    with pytest.raises(DeepSeekRequestError, match="模型或请求参数") as error:
        asyncio.run(chat_with_deepseek("test"))

    assert error.value.status_code == 400
    assert "test-key" not in str(error.value)


def test_rate_limited_response_is_not_reported_as_a_generic_failure(monkeypatch):
    configure_live_provider(monkeypatch)
    response = httpx.Response(
        429,
        json={"error": {"message": "rate limit exceeded"}},
        request=httpx.Request("POST", "https://api.deepseek.com/v1/chat/completions"),
    )
    monkeypatch.setattr("services.deepseek.httpx.AsyncClient", lambda: FakeAsyncClient(response=response))

    with pytest.raises(DeepSeekRequestError, match="请求过于频繁") as error:
        asyncio.run(chat_with_deepseek("test"))

    assert error.value.status_code == 429


def test_timeout_is_reported_as_a_retryable_service_error(monkeypatch):
    configure_live_provider(monkeypatch)
    monkeypatch.setattr(
        "services.deepseek.httpx.AsyncClient",
        lambda: FakeAsyncClient(exception=httpx.TimeoutException("timeout")),
    )

    with pytest.raises(DeepSeekRequestError, match="请求超时") as error:
        asyncio.run(chat_with_deepseek("test"))

    assert error.value.status_code == 504
