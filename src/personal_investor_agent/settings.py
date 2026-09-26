from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    investor_db_host: str = "postgres"
    investor_db_port: int = 5432
    investor_db: str
    investor_db_user: str
    investor_db_password: SecretStr


@lru_cache
def get_settings() -> Settings:
    return Settings()
