#!/usr/bin/env bash

use_sops() {
    local secrets_file
    secrets_file="$1"

    if [[ -f $secrets_file ]]; then
        eval "$(sops --decrypt "$secrets_file" | direnv dotenv bash /dev/stdin)"
        watch_file "$secrets_file"
    else
        log_status "Error: Secrets file '$secrets_file' not found." >&2
        return 1
    fi
}
