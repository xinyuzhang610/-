import pytest
from config import settings

def test_settings_loads():
    assert settings.APP_NAME == "智教通"
    assert settings.APP_VERSION == "1.0.0"
    assert settings.DEBUG is True

def test_database_url():
    assert "mysql+pymysql://" in settings.DATABASE_URL

def test_deepseek_config():
    assert settings.DEEPSEEK_MODEL == "dsv4"
    assert "deepseek" in settings.DEEPSEEK_API_URL.lower()

def test_cors_origins():
    assert isinstance(settings.CORS_ORIGINS, list)
    assert len(settings.CORS_ORIGINS) > 0