# AI Engineering
### AI FROM SCRATCH

A reproducible learning workspace for Python, TypeScript, Rust, and AI engineering.
The language toolchains run in Docker; lesson files live under `workspace/` on the host.

## Start here

1. Install Docker Desktop (macOS/Windows) or Docker Engine with the Compose plugin (Linux).
2. Build and start the development container. It installs the Python requirements,
   runs the NumPy demo and first course lesson, then opens a shell:

   ```sh
   docker compose up --build
   ```

3. To run the Python demo again:

   ```sh
   ./run-python.sh workspace/python/numpy_demo.py
   ```

The container creates a project virtual environment in the mounted workspace and installs
`workspace/python/requirements.txt` at startup. It runs the NumPy setup demo and
`phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py` each time it starts.
Stop the container with `docker compose down`.

## Lesson 1: Development environment

See [the environment setup lesson](phases/00-setup-and-tooling/01-dev-environment/README.md).
Use the route preflight from this repository root:

```sh
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route beginner
```

Run `--help` to see all supported routes. `--show-later` includes optional tools used in
later lessons; those checks do not block the selected route.
