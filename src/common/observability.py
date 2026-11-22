import os

import logfire

from src.common.settings import settings

OTEL_SERVICE_NAME = "homelab-agent"
OTEL_PROTOCOL = "http/protobuf"


def configure_observability() -> bool:
    if settings.OTEL_AUTH_TOKEN is None or settings.OTEL_EXPORTER_OTLP_ENDPOINT is None:
        return False

    token = settings.OTEL_AUTH_TOKEN.get_secret_value()
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = settings.OTEL_EXPORTER_OTLP_ENDPOINT
    os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = OTEL_PROTOCOL
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Bearer {token}"

    logfire.configure(
        service_name=OTEL_SERVICE_NAME,
        send_to_logfire=False,
        metrics=False,
    )
    logfire.instrument_pydantic_ai()
    logfire.instrument_httpx(capture_headers=False)

    return True
