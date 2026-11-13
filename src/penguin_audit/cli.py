"""Command-line entry point for penguin-audit."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from penguin_audit import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser (separated so tests can reuse it)."""
    parser = argparse.ArgumentParser(
        prog="penguin-audit",
        description="A read-only Linux security auditor.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"penguin-audit {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. Returns a process exit code."""
    parser = build_parser()
    parser.parse_args(argv)
    return 0
