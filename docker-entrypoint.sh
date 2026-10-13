#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x /workspace/.venv/bin/python ]]; then
    uv venv --python 3.12 /workspace/.venv
fi
uv pip install --python /workspace/.venv/bin/python \
    -r /workspace/python/requirements.txt

printf '\nRunning the Python starter demo...\n'
/workspace/.venv/bin/python /workspace/python/numpy_demo.py

printf '\nRunning the first course lesson...\n'
/workspace/.venv/bin/python \
    /course/phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py

printf '\nDemo finished. The container is ready for interactive work.\n'
exec bash
