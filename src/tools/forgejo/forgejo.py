from typing import Any

import httpx
from pydantic import TypeAdapter

from src.common import settings
from src.tools.forgejo.constants import MAX_RESULTS, NAME_RE
from src.tools.forgejo.entities import Commit, Issue, PullRequest
from src.tools.forgejo.exceptions import InvalidName, RepositoryNotFound


async def _fetch_repository_resource[T](
    *,
    http: httpx.AsyncClient,
    owner: str,
    repo: str,
    resource: str,
    params: dict[str, Any],
    adapter: TypeAdapter[T],
) -> T:
    for name in (owner, repo):
        if not NAME_RE.match(name):
            raise InvalidName(f"Nombre inválido: {name!r}")

    response = await http.get(
        url=f"{settings.FORGEJO_URL}/api/v1/repos/{owner}/{repo}/{resource}",
        params=params,
        headers={"Authorization": f"token {settings.FORGEJO_TOKEN.get_secret_value()}"},
    )

    if response.status_code == 404:
        raise RepositoryNotFound(f"Repositorio '{owner}/{repo}' no encontrado.")

    response.raise_for_status()

    return adapter.validate_json(response.content)


async def list_open_pull_requests(
    *,
    http: httpx.AsyncClient,
    owner: str,
    repo: str,
) -> list[PullRequest]:
    return await _fetch_repository_resource(
        http=http,
        owner=owner,
        repo=repo,
        resource="pulls",
        params={"state": "open", "limit": MAX_RESULTS},
        adapter=TypeAdapter(list[PullRequest]),
    )


async def list_open_issues(
    *,
    http: httpx.AsyncClient,
    owner: str,
    repo: str,
) -> list[Issue]:
    return await _fetch_repository_resource(
        http=http,
        owner=owner,
        repo=repo,
        resource="issues",
        params={"state": "open", "type": "issues", "limit": MAX_RESULTS},
        adapter=TypeAdapter(list[Issue]),
    )


async def list_recent_commits(
    *,
    http: httpx.AsyncClient,
    owner: str,
    repo: str,
    branch: str,
    limit: int,
) -> list[Commit]:
    if not NAME_RE.match(branch):
        raise InvalidName(f"Rama inválida: {branch!r}")

    return await _fetch_repository_resource(
        http=http,
        owner=owner,
        repo=repo,
        resource="commits",
        params={
            "sha": branch,
            "limit": min(limit, MAX_RESULTS),
            "stat": "false",
            "verification": "false",
            "files": "false",
        },
        adapter=TypeAdapter(list[Commit]),
    )
