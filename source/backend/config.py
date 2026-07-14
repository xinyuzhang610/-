from pydantic_settings import BaseSettings
from typing import List, Literal

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "智教通"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "development-only-change-me"
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://zjiaotong_app:change-me@127.0.0.1:3306/zjiaotong"
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_API_URL: str = "https://api.deepseek.com"
    AI_PROVIDER: Literal["mock", "deepseek"] = "mock"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
