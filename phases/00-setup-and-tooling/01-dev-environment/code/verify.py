#!/usr/bin/env python3
"""Check the host tools and lesson files needed for a learning route."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


@dataclass(frozen=True)
class Check:
    label: str
    command: str
    fix: str


ROUTES: dict[str, tuple[Check, ...]] = {
    "beginner": (
        Check("Docker", "docker", "Install Docker Desktop or Docker Engine."),
        Check("Docker Compose", "docker compose version", "Install the Docker Compose plugin."),
        Check("Docker daemon", "docker info", "Start Docker Desktop or the Docker Engine service."),
    ),
    "ml-foundations": (
        Check("Docker", "docker", "Install Docker Desktop or Docker Engine."),
        Check("Docker Compose", "docker compose version", "Install the Docker Compose plugin."),
    ),
    "llm-engineering": (
        Check("Docker", "docker", "Install Docker Desktop or Docker Engine."),
        Check("Docker Compose", "docker compose version", "Install the Docker Compose plugin."),
    ),
    "agents": (
        Check("Docker", "docker", "Install Docker Desktop or Docker Engine."),
        Check("Docker Compose", "docker compose version", "Install the Docker Compose plugin."),
    ),
    "mcp": (
        Check("Docker", "docker", "Install Docker Desktop or Docker Engine."),
        Check("Docker Compose", "docker compose version", "Install the Docker Compose plugin."),
    ),
    "agent-skills": (
        Check("Docker", "docker", "Install Docker Desktop or Docker Engine."),
        Check("Docker Compose", "docker compose version", "Install the Docker Compose plugin."),
    ),
    "certification": (
        Check("Docker", "docker", "Install Docker Desktop or Docker Engine."),
        Check("Docker Compose", "docker compose version", "Install the Docker Compose plugin."),
    ),
}

LATER = (
    Check("Git", "git", "Install Git from https://git-scm.com/."),
    Check("Python 3", "python3", "Install Python 3.11 or newer."),
    Check("uv", "uv", "Install uv: https://docs.astral.sh/uv/getting-started/installation/."),
    Check("Node.js", "node", "Install Node.js 20 or newer."),
    Check("pnpm", "pnpm", "Install pnpm: https://pnpm.io/installation."),
    Check("Rust", "rustc", "Install Rust with rustup: https://rustup.rs/."),
    Check("Julia", "julia", "Install Julia: https://julialang.org/downloads/."),
)


def run_check(check: Check) -> tuple[bool, str]:
    parts = check.command.split()
    executable = parts[0]
    if shutil.which(executable) is None:
        return False, f"{check.label}: missing. Fix: {check.fix}"
    try:
        result = subprocess.run(
            parts, check=False, capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, f"{check.label}: could not run ({error}). Fix: {check.fix}"
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        suffix = f" ({detail[-1]})" if detail else ""
        return False, f"{check.label}: command failed{suffix}. Fix: {check.fix}"
    version = (result.stdout or result.stderr).strip().splitlines()
    description = f" ({version[0]})" if version else ""
    return True, f"{check.label}: OK{description}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route", choices=sorted(ROUTES), default="beginner")
    parser.add_argument(
        "--show-later",
        action="store_true",
        help="also inspect optional tools for later lessons (informational only)",
    )
    args = parser.parse_args()

    required = list(ROUTES[args.route])
    missing = False
    print(f"Preflight route: {args.route}")
    for check in required:
        passed, message = run_check(check)
        print(f"{'✓' if passed else '✗'} {message}")
        missing |= not passed

    if args.route == "beginner":
        files = (
            (ROOT / "Dockerfile", "Restore the repository Dockerfile."),
            (ROOT / "compose.yaml", "Restore the repository Compose file."),
            (ROOT / "docker-entrypoint.sh", "Restore the automatic Python startup script."),
            (ROOT / "run-python.sh", "Restore the Python runner script."),
            (ROOT / "workspace/python/numpy_demo.py", "Restore the NumPy demo."),
            (ROOT / "workspace/python/requirements.txt", "Restore the Python requirements file."),
            (ROOT / "phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py",
             "Restore the first runnable lesson."),
        )
        for path, fix in files:
            passed = path.is_file()
            print(f"{'✓' if passed else '✗'} {path.relative_to(ROOT)}: "
                  f"{'OK' if passed else f'missing. Fix: {fix}'}")
            missing |= not passed

    if args.show_later:
        print("\nOptional later tools (these do not block this route):")
        for check in LATER:
            passed, message = run_check(check)
            print(f"{'✓' if passed else '·'} {message}")

    if args.route in {"agent-skills", "certification"}:
        print("\nManual check: confirm your AI host has discovered the required skill.")
        print("Manual check: confirm the intended skill scope is writable.")

    if missing:
        print("\nPreflight failed. Apply the corrective commands above and rerun this check.")
        return 1

    if args.route == "beginner":
        print("\nPreflight passed. First runnable lesson:")
        print("docker compose up --build")
        print("Next lesson runs automatically: "
              "phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py")
    else:
        print(f"\nPreflight passed for route: {args.route}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
