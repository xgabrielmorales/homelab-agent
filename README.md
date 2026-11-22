# Homelab Agent

AI agent that knows what is happening in my homelab. It reads the k3s cluster, Grafana and Forgejo, answers questions through a web chat that is only reachable from the LAN or the WireGuard VPN, and sends a daily report as a push notification.

> [!NOTE]
> This is built for [my homelab](https://github.com/xgabrielmorales/homelab), not as a product for public use. The prompts, tools and defaults assume its setup.

## Features

- **Chat**: ask about the homelab from the browser. The web chat is only reachable from the LAN or the WireGuard VPN.
- **Daily report**: a 07:00 summary of the homelab's health, pushed to Gotify.
- **Read-only**: it can look at everything and change nothing. Logs, events and PRs are treated as data, never as instructions.
- **Observability**: connect it to your OpenTelemetry stack to trace every run and track tokens and cost.

## Architecture

A single [pydantic-ai](https://ai.pydantic.dev) agent on OpenAI GPT 6.1 Terra through [OpenRouter](https://openrouter.ai). A Starlette app serves the pydantic-ai web chat and, in the background, runs the daily report.

| Tool                                                  | Source                                  | Use                                                 |
| ----------------------------------------------------- | --------------------------------------- | --------------------------------------------------- |
| Grafana MCP (`mcp-grafana`)                           | Prometheus, Loki, alerts and dashboards | Metrics, logs and active alerts                     |
| Kubernetes MCP (`kubernetes-mcp-server`)              | Kubernetes API                          | Pods, events, logs, Flux resources and memory usage |
| `open_pull_requests`, `open_issues`, `recent_commits` | Forgejo API                             | Pending Renovate PRs and recent changes to `trunk`  |

Everything is read-only: the MCP servers run with their write tools disabled, the Kubernetes service account is bound to the `view` role (no Secrets) and the Forgejo token only has read scopes. The only write is the report, which the code (not the agent) publishes to Gotify, so a log or a PR that tries to instruct the agent cannot send anything.
