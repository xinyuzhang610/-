import pytest
import pytest

from config import Settings, settings
from services.deepseek import AIConfigurationError, chat_with_deepseek

def test_settings_loads():
    assert settings.APP_NAME == "智教通"
    assert settings.APP_VERSION == "1.0.0"
    assert settings.DEBUG is True

def test_database_url():
    assert "mysql+pymysql://" in settings.DATABASE_URL

def test_deepseek_config():
    assert settings.DEEPSEEK_MODEL
    assert "deepseek" in settings.DEEPSEEK_API_URL.lower()

def test_cors_origins():
    assert isinstance(settings.CORS_ORIGINS, list)
    assert len(settings.CORS_ORIGINS) > 0


def test_live_ai_requires_a_key(monkeypatch):
    monkeypatch.setattr("services.deepseek.settings", Settings(AI_PROVIDER="deepseek", DEEPSEEK_API_KEY=""))

    with pytest.raises(AIConfigurationError):
        import asyncio
        asyncio.run(chat_with_deepseek("测试"))
