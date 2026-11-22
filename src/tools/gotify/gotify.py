import httpx

from src.common import settings


async def publish(
    *,
    http: httpx.AsyncClient,
    title: str,
    message: str,
    priority: int = 5,
) -> None:
    response = await http.post(
        url=f"{settings.GOTIFY_URL}/message",
        json={
            "title": title,
            "message": message,
            "priority": priority,
            "extras": {"client::display": {"contentType": "text/markdown"}},
        },
        headers={"X-Gotify-Key": settings.GOTIFY_TOKEN.get_secret_value()},
    )
    response.raise_for_status()
