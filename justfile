registry := "git.xgabrielmorales.com/xgabrielmorales/homelab-agent"

publish:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "$(git status --porcelain)" ]]; then
        echo "Commit your changes first: the image tag must match a commit." >&2
        exit 1
    fi
    image="{{ registry }}:$(git rev-parse HEAD)"
    docker build --platform linux/amd64 --file environment/prod/Dockerfile --tag "$image" .
    docker push "$image"
    docker image inspect --format '{{{{ index .RepoDigests 0 }}' "$image"
