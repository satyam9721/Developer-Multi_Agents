from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.config.constants import LLMProvider

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "Multi-Agent System"
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True

    WORKSPACE_ROOT: str = "./workspace"

    DATABASE_URL: Optional[str] = "postgresql+asyncpg://postgres:postgres@localhost:5432/multi_agent_db"
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"

    LLM_PROVIDER: str = LLMProvider.MOCK
    LLM_MODEL: str = "mock-v1"
    LLM_API_KEY: Optional[str] = None

    GITHUB_TOKEN: Optional[str] = None
    GITHUB_API_URL: str = "https://api.github.com"

    CELERY_BROKER_URL: Optional[str] = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: Optional[str] = "redis://localhost:6379/2"

settings = Settings()
