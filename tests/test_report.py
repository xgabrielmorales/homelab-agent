import asyncio
import json
from datetime import datetime, time
from zoneinfo import ZoneInfo

import httpx
import pytest
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import ModelMessage, ModelResponse
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.models.test import TestModel

from src.agents.homelab.agent import homelab_agent
from src.agents.homelab.report import publish_daily_report, seconds_until

BOGOTA = ZoneInfo("America/Bogota")
NEW_YORK = ZoneInfo("America/New_York")


@pytest.mark.parametrize(
    ("now", "expected"),
    [
        (datetime(2026, 11, 21, 6, 0, tzinfo=BOGOTA), 3600),
        (datetime(2026, 11, 21, 7, 0, tzinfo=BOGOTA), 24 * 3600),
        (datetime(2026, 11, 21, 23, 0, tzinfo=BOGOTA), 8 * 3600),
        (datetime(2026, 3, 7, 7, 0, tzinfo=NEW_YORK), 23 * 3600),
    ],
)
def test_seconds_until(now: datetime, expected: float) -> None:
    assert seconds_until(time(7, 0), now) == expected


def publish_with(model: TestModel | FunctionModel) -> dict[str, object]:
    published_messages: list[dict[str, object]] = []

    def ntfy(request: httpx.Request) -> httpx.Response:
        published_messages.append(json.loads(request.content))
        return httpx.Response(200)

    async def run_report() -> None:
        async with httpx.AsyncClient(transport=httpx.MockTransport(ntfy)) as http:
            with homelab_agent.override(model=model, toolsets=[]):
                await publish_daily_report(http)

    asyncio.run(run_report())
    assert len(published_messages) == 1
    return published_messages[0]


def test_publishes_report_with_status_priority() -> None:
    published = publish_with(
        TestModel(call_tools=[], custom_output_args={"status": "critico", "summary": "Loki caído"})
    )
    assert published["title"] == "Homelab: critico"
    assert published["message"] == "Loki caído"
    assert published["priority"] == 5


def test_notifies_when_report_fails() -> None:
    def fail(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        raise UnexpectedModelBehavior("respuesta inválida")

    published = publish_with(FunctionModel(fail))
    assert published["title"] == "Homelab: reporte fallido"
    assert published["priority"] == 4
