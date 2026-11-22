import asyncio
from datetime import UTC, datetime, time, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

import httpx
import logfire
from fastmcp.exceptions import ClientError, FastMCPError
from pydantic_ai.exceptions import AgentRunError
from pydantic_ai.mcp import MCPError
from pydantic_ai.usage import UsageLimits

from src.agents.homelab.agent import homelab_agent
from src.agents.homelab.constants import DAILY_REPORT_PROMPT, MAX_MODEL_REQUESTS
from src.agents.homelab.entities import DailyReport
from src.common import settings
from src.tools import Deps
from src.tools.ntfy import publish

PRIORITY_BY_STATUS: dict[str, Literal[1, 2, 3, 4, 5]] = {
    "ok": 2,
    "atencion": 3,
    "critico": 5,
}


def seconds_until(at: time, now: datetime) -> float:
    target = datetime.combine(now.date(), at, tzinfo=now.tzinfo)
    if target <= now:
        target = datetime.combine(now.date() + timedelta(days=1), at, tzinfo=now.tzinfo)
    return (target.astimezone(UTC) - now.astimezone(UTC)).total_seconds()


async def publish_daily_report(http: httpx.AsyncClient) -> None:
    with logfire.span("daily report"):
        try:
            result = await homelab_agent.run(
                DAILY_REPORT_PROMPT,
                deps=Deps(async_http_client=http),
                output_type=DailyReport,
                usage_limits=UsageLimits(request_limit=MAX_MODEL_REQUESTS),
            )
        except (AgentRunError, MCPError, FastMCPError, ClientError, httpx.HTTPError) as error:
            logfire.exception("daily report failed")
            await publish(
                http=http,
                title="Homelab: reporte fallido",
                message=f"No se pudo generar el reporte diario: {type(error).__name__}.",
                priority=4,
            )
            return

        report = result.output
        await publish(
            http=http,
            title=f"Homelab: {report.status}",
            message=report.summary,
            priority=PRIORITY_BY_STATUS[report.status],
        )


async def schedule_daily_report(http: httpx.AsyncClient) -> None:
    zone = ZoneInfo(settings.TIMEZONE)
    while True:
        await asyncio.sleep(seconds_until(settings.REPORT_TIME, datetime.now(zone)))
        try:
            await publish_daily_report(http)
        except httpx.HTTPError:
            logfire.exception("failed to publish the report to ntfy")
