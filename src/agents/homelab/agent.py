from pydantic_ai import Agent, Tool
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from src.agents.homelab.constants import INSTRUCTIONS
from src.common import settings
from src.tools import Deps, open_issues, open_pull_requests, recent_commits

model = OpenRouterModel(
    settings.MODEL,
    provider=OpenRouterProvider(
        api_key=settings.OPENROUTER_API_KEY.get_secret_value(),
        app_title="homelab-agent",
    ),
)

homelab_agent = Agent(
    model,
    deps_type=Deps,
    instructions=INSTRUCTIONS,
    toolsets=[
        MCPToolset(settings.GRAFANA_MCP_URL, id="grafana"),
        MCPToolset(settings.KUBERNETES_MCP_URL, id="kubernetes"),
    ],
    tools=[
        Tool(tool, docstring_format="google", require_parameter_descriptions=True)
        for tool in (open_pull_requests, open_issues, recent_commits)
    ],
)
