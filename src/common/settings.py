from datetime import time
from pathlib import Path
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
    TIMEZONE: str = "America/Bogota"

    OPENROUTER_API_KEY: SecretStr
    MODEL: str = "openai/gpt-6.1-terra"

    FORGEJO_URL: str
    FORGEJO_TOKEN: SecretStr

    GRAFANA_MCP_URL: str = "http://127.0.0.1:8001/mcp"
    KUBERNETES_MCP_URL: str = "http://127.0.0.1:8002/mcp"

    GOTIFY_URL: str
    GOTIFY_TOKEN: SecretStr

    REPORT_TIME: time = time(7, 0)

    OTEL_AUTH_TOKEN: SecretStr | None = None
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = None

    UVICORN_HOST: str = "127.0.0.1"
    UVICORN_PORT: int = 8000
    UVICORN_WORKERS: int = 1
    ALLOWED_HOSTS: list[str] = []
    CHAT_UI_HTML: Path | None = None


settings = Settings()  # type: ignore[call-arg]
