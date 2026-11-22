FROM dhi.io/python:3.14.8-debian13-dev@sha256:2a80fcc0afb4883d61da0650c817600b000d455dcea7c81212b32c94e7c7e244 AS builder

ENV \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/venv \
    UV_PYTHON=python3 \
    UV_PYTHON_DOWNLOADS=never

RUN \
    --mount=from=ghcr.io/astral-sh/uv:0.13.1,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./pyproject.toml,target=./pyproject.toml \
    --mount=type=bind,source=./uv.lock,target=./uv.lock \
    uv sync --locked --no-dev --no-install-project

FROM dhi.io/python:3.14.8-debian13@sha256:4cf31b8a8d9c477b2f22f53d6f61df647efadf792084863a2b6397833db20c54

ENV \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

ARG \
    GROUP_ID="65532" \
    USER_ID="65532"

WORKDIR /app

COPY --from=builder /venv /venv

COPY --chown="${USER_ID}:${GROUP_ID}" ./src ./src

USER "${USER_ID}:${GROUP_ID}"
