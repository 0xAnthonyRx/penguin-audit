"""Runner: execute checks, capture errors, return structured results."""

from __future__ import annotations

import time
import traceback

from penguin_audit.core.models import CheckResult
from penguin_audit.core.registry import all_checks, get_check


def run_check(name: str) -> CheckResult:
    """Run one named check and return a CheckResult.

    If the check raises, the exception is captured into `error` and `traceback`
    instead of propagating — a broken check must not crash the whole audit.
    """
    func = get_check(name)  # KeyError if unknown — a user error, let it propagate
    started = time.perf_counter()
    try:
        findings = func()
    except Exception as exc:  # noqa: BLE001 — a broken check must not crash the audit
        duration_ms = (time.perf_counter() - started) * 1000
        return CheckResult(
            check=name,
            duration_ms=duration_ms,
            error=f"{type(exc).__name__}: {exc}",
            traceback=traceback.format_exc(),
        )
    duration_ms = (time.perf_counter() - started) * 1000
    return CheckResult(check=name, findings=findings, duration_ms=duration_ms)


def run_checks(names: list[str] | None = None) -> list[CheckResult]:
    """Run the named checks, or all registered checks if names is None."""
    # Importing this package triggers every @register decorator to run.
    import penguin_audit.checks  # noqa: F401

    targets = names if names is not None else list(all_checks())
    return [run_check(n) for n in targets]
