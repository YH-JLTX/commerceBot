"""
====================================
代码任务: 核心配置模块
最后修改: 2026-03-30 20:00
====================================
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    # 应用配置
    APP_NAME: str = "CommerceBot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8765

    # 数据库配置
    DATABASE_URL: str = "mysql+aiomysql://root:123456@localhost:3306/commerce_bot?charset=utf8mb4"

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:3445", "http://localhost:3446"]

    # LLM配置
    OPENROUTER_API_KEY: str = "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"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
