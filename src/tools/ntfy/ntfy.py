from typing import Literal

import httpx

from src.common import settings
from src.tools.ntfy.constants import MAX_MESSAGE_BYTES, TRUNCATION_MARK


def truncate_message(message: str) -> str:
    if len(message.encode()) <= MAX_MESSAGE_BYTES:
        return message
    available = MAX_MESSAGE_BYTES - len(TRUNCATION_MARK.encode())
    return message.encode()[:available].decode(errors="ignore") + TRUNCATION_MARK


async def publish(
    *,
    http: httpx.AsyncClient,
    title: str,
    message: str,
    priority: Literal[1, 2, 3, 4, 5] = 3,
) -> None:
    response = await http.post(
        url=settings.NTFY_URL,
        json={
            "topic": settings.NTFY_TOPIC,
            "title": title,
            "message": truncate_message(message),
            "priority": priority,
            "markdown": True,
        },
        headers={"Authorization": f"Bearer {settings.NTFY_TOKEN.get_secret_value()}"},
    )
    response.raise_for_status()
