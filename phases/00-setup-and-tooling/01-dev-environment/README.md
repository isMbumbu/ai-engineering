# Development Environment

**Prerequisites:** None · **Time:** about 45 minutes

## Learning objectives

- Set up Python 3.11+, Node.js 20+, and Rust toolchains.
- Use virtual environments and package managers for reproducible builds.
- Check CUDA or Apple MPS availability and run a tensor operation.
- Explain the environment's four layers: system, package managers, runtimes, and AI libraries.

## The four-layer stack

Build from the bottom up: the system and GPU drivers support package managers; package
managers install language runtimes; runtimes host the AI libraries. When an import fails,
check each layer from the bottom upward.

| Layer | Examples |
| --- | --- |
| System foundation | OS, shell, Git, editor, GPU drivers |
| Package managers | `uv`, `pnpm`, `cargo`, `juliaup` |
| Language runtimes | Python, Node.js, Rust, Julia |
| AI/ML libraries | PyTorch, JAX, Transformers |

## Use this repository's Docker environment

This project includes Python 3.12, Node.js 22, Rust, Git, and build tools in its Docker
image. Python 3.12 satisfies the Python 3.11+ objective; Node.js 22 satisfies Node.js 20+.
You don't need to install those toolchains on the host. Docker itself and the host's GPU
drivers remain host requirements.

From the repository root:

```sh
docker compose up --build
```

The first startup builds the image, installs the Python requirements, runs the NumPy demo
and first course lesson (`phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py`),
then opens a shell. Both examples run again whenever the container starts. Inside the shell,
check the toolchains:

```sh
python3 --version
uv --version
node --version
pnpm --version
rustc --version
cargo --version
git --version
```

The first course exercise is [vectors.py](../../01-math-foundations/01-linear-algebra-intuition/code/vectors.py).
The setup example is available at `workspace/python/numpy_demo.py`. Run that setup example
again with `./run-python.sh workspace/python/numpy_demo.py`. Dependencies are listed in
`workspace/python/requirements.txt`.

## GPU access

GPU access comes from the host and its drivers; installing a package in a container alone
does not enable it. CPU PyTorch works for the first exercises. On Linux with an NVIDIA GPU,
configure the NVIDIA Container Toolkit and a CUDA-enabled container before requesting GPU
access. Docker Desktop containers generally cannot access macOS Metal/MPS directly, so use
a native macOS Python environment for Apple Silicon MPS lessons. Windows GPU lessons use
WSL2, NVIDIA drivers, and Docker GPU support. CPU-only learners can use CPU builds or a cloud
GPU.

## Optional native setup

If you're following this lesson outside Docker, install system build tools, Git, and `curl`
first. On Ubuntu/Debian/WSL2:

```sh
sudo apt update
sudo apt install -y build-essential git curl wget unzip
```

Install Python with `uv`, Node.js with `fnm`, and Rust with `rustup` using their official
installers. Create a per-project environment with `uv venv`, activate it, then install
NumPy, Matplotlib, and Jupyter. On macOS, use the plain PyTorch packages for MPS; CUDA
packages are for compatible NVIDIA systems. Run `python3 -m` commands from the project
environment when using this native setup.

## Preflight

Run the preflight at the repository root. It checks only the tools needed for the selected
route; `--show-later` adds informational checks for later lessons.

```sh
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route beginner
```

Available routes: `beginner`, `ml-foundations`, `llm-engineering`, `agents`, `mcp`,
`agent-skills`, and `certification`. Agent Skills and certification routes also include
manual checks, since a script cannot verify that an AI host has discovered a skill or that
the intended skill scope is writable.
