#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s workspace/path/to/script.py\n' "$0" >&2
    exit 2
fi

project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
workspace_root="$project_root/workspace"
source_file="$1"

if [[ "$source_file" != /* ]]; then
    source_file="$project_root/$source_file"
fi

case "$source_file" in
    "$workspace_root"/*) ;;
    *)
        printf 'Python files must be under %s\n' "$workspace_root" >&2
        exit 2
        ;;
esac

if [[ ! -f "$source_file" ]]; then
    printf 'Python file not found: %s\n' "$source_file" >&2
    exit 2
fi

container_file="/workspace/${source_file#"$workspace_root/"}"

cd "$project_root"
docker compose up -d --build ai-dev
docker compose exec -T ai-dev bash -lc '
    uv venv --python 3.12 /workspace/.venv
    uv pip install --python /workspace/.venv/bin/python -r /workspace/python/requirements.txt
    exec /workspace/.venv/bin/python "$1"
' -- "$container_file"