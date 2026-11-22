FROM dhi.io/python:3.14.8-debian13-dev@sha256:2a80fcc0afb4883d61da0650c817600b000d455dcea7c81212b32c94e7c7e244

ENV \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/venv \
    UV_PYTHON=python3 \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/venv/bin:$PATH"

ARG \
    APP_NAME="agent" \
    GROUP_ID="1000" \
    USER_ID="1000"

RUN echo "${APP_NAME}:x:${GROUP_ID}:" >> /etc/group \
    && echo "${APP_NAME}:x:${USER_ID}:${GROUP_ID}::/home/${APP_NAME}:/sbin/nologin" >> /etc/passwd

RUN \
    --mount=from=ghcr.io/astral-sh/uv:0.13.1,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./pyproject.toml,target=./pyproject.toml \
    --mount=type=bind,source=./uv.lock,target=./uv.lock \
    uv sync --locked --no-install-project

ADD \
    --chmod=644 \
    --checksum=sha256:18ad2ee902620e4c3e089a2979bc822612db31e0db48fde8e759aa78ce79f7f8 \
    https://cdn.jsdelivr.net/npm/@pydantic/ai-chat-ui@2.1.0/offline/index.html \
    /opt/chat-ui.html

ENV CHAT_UI_HTML=/opt/chat-ui.html

WORKDIR /app

USER "${APP_NAME}"
