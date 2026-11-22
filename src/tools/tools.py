from dataclasses import dataclass

import httpx
from pydantic_ai import RunContext

from src.tools.forgejo import (
    Commit,
    InvalidName,
    Issue,
    PullRequest,
    RepositoryNotFound,
    list_open_issues,
    list_open_pull_requests,
    list_recent_commits,
)


@dataclass
class Deps:
    async_http_client: httpx.AsyncClient


def _error_message(owner: str, repo: str, error: Exception) -> str:
    if isinstance(error, RepositoryNotFound):
        return f"El repositorio '{owner}/{repo}' no existe en Forgejo o el token no tiene acceso."
    return f"{error}. Usa solo letras, números, '.', '_' o '-'."


async def open_pull_requests(
    ctx: RunContext[Deps],
    owner: str = "xgabrielmorales",
    repo: str = "homelab",
) -> list[PullRequest] | str:
    """Pull requests abiertos de un repositorio en el Forgejo del homelab.

    En el repo 'homelab' casi todos los abre Renovate para actualizar imágenes y charts; uno
    abierto hace días es una actualización pendiente de revisar.

    Args:
        ctx: Contexto de la ejecución, con el cliente HTTP.
        owner: Dueño del repositorio.
        repo: Nombre del repositorio.

    Returns:
        Los pull requests abiertos, o un mensaje si no hay ninguno, si el repositorio no existe o
        si el nombre no es válido.
    """
    try:
        pull_requests = await list_open_pull_requests(
            http=ctx.deps.async_http_client,
            owner=owner,
            repo=repo,
        )
        return pull_requests or f"No hay pull requests abiertos en '{owner}/{repo}'."
    except (RepositoryNotFound, InvalidName) as error:
        return _error_message(owner, repo, error)


async def open_issues(
    ctx: RunContext[Deps],
    owner: str = "xgabrielmorales",
    repo: str = "homelab",
) -> list[Issue] | str:
    """Issues abiertos (sin contar pull requests) de un repositorio en el Forgejo del homelab.

    Args:
        ctx: Contexto de la ejecución, con el cliente HTTP.
        owner: Dueño del repositorio.
        repo: Nombre del repositorio.

    Returns:
        Los issues abiertos, o un mensaje si no hay ninguno, si el repositorio no existe o si el
        nombre no es válido.
    """
    try:
        issues = await list_open_issues(
            http=ctx.deps.async_http_client,
            owner=owner,
            repo=repo,
        )
        return issues or f"No hay issues abiertos en '{owner}/{repo}'."
    except (RepositoryNotFound, InvalidName) as error:
        return _error_message(owner, repo, error)


async def recent_commits(
    ctx: RunContext[Deps],
    owner: str = "xgabrielmorales",
    repo: str = "homelab",
    branch: str = "trunk",
    limit: int = 10,
) -> list[Commit] | str:
    """Commits más recientes de una rama, del más nuevo al más viejo.

    En el repo 'homelab', Flux despliega la rama 'trunk' en el cluster: sus commits recientes
    explican cambios recientes en el cluster.

    Args:
        ctx: Contexto de la ejecución, con el cliente HTTP.
        owner: Dueño del repositorio.
        repo: Nombre del repositorio.
        branch: Rama a consultar.
        limit: Cuántos commits devolver, como máximo 50.

    Returns:
        Los commits, o un mensaje si la rama no tiene commits, si el repositorio no existe o si
        algún nombre no es válido.
    """
    try:
        commits = await list_recent_commits(
            http=ctx.deps.async_http_client,
            owner=owner,
            repo=repo,
            branch=branch,
            limit=limit,
        )
        return commits or f"La rama '{branch}' de '{owner}/{repo}' no tiene commits."
    except (RepositoryNotFound, InvalidName) as error:
        return _error_message(owner, repo, error)
