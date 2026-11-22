from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    OTEL_AUTH_TOKEN: SecretStr | None = None
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = None

    UVICORN_HOST: str = "127.0.0.1"
    UVICORN_PORT: int = 8000
    UVICORN_WORKERS: int = 1


settings = Settings()
