#!/usr/bin/env bash

use_uv() {
    local venv_path

    if [[ -d ".venv" ]]; then
        venv_path="$PWD/.venv"
    fi

    if [[ -z $venv_path || ! -d $venv_path ]]; then
        log_status "No virtual environment found. Running 'uv sync'..."
        uv sync
        venv_path="$PWD/.venv"
    fi

    if [[ -d ".venv/bin" ]]; then
        PATH_add ".venv/bin"
    fi

    export UV_ACTIVE=1
    export VIRTUAL_ENV="$venv_path"
}
