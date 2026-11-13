"""Ensure the package imports cleanly and `--version` works."""

import subprocess
import sys

from penguin_audit import __version__


def test_version_is_a_nonempty_string() -> None:
    assert isinstance(__version__, str)
    assert __version__


def test_cli_version_flag_via_subprocess() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "penguin_audit", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "penguin-audit" in result.stdout
    assert __version__ in result.stdout
