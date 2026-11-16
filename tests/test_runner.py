"""Tests for the check runner."""

import pytest

from penguin_audit.core import registry
from penguin_audit.core.models import Finding, Severity
from penguin_audit.core.runner import run_check, run_checks


@pytest.fixture(autouse=True)
def clean_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(registry, "_REGISTRY", {})


def _finding(check: str = "x") -> Finding:
    return Finding(
        check=check,
        code="X001",
        severity=Severity.LOW,
        title="t",
        description="d",
    )


def test_run_check_happy_path() -> None:
    @registry.register("ok")
    def ok() -> list[Finding]:
        return [_finding("ok")]

    result = run_check("ok")
    assert result.ok is True
    assert result.findings == [_finding("ok")]
    assert result.duration_ms >= 0
    assert result.error is None
    assert result.traceback == ""


def test_run_check_captures_exception() -> None:
    @registry.register("boom")
    def boom() -> list[Finding]:
        raise RuntimeError("kaboom")

    result = run_check("boom")
    assert result.ok is False
    assert result.error is not None
    assert "RuntimeError" in result.error
    assert "kaboom" in result.error
    assert "RuntimeError" in result.traceback
    assert result.findings == []


def test_run_checks_runs_all_by_default() -> None:
    @registry.register("a")
    def a() -> list[Finding]:
        return []

    @registry.register("b")
    def b() -> list[Finding]:
        return []

    results = run_checks()
    assert {r.check for r in results} == {"a", "b"}


def test_run_checks_with_subset() -> None:
    @registry.register("a")
    def a() -> list[Finding]:
        return []

    @registry.register("b")
    def b() -> list[Finding]:
        return []

    results = run_checks(["b"])
    assert len(results) == 1
    assert results[0].check == "b"


def test_run_checks_isolates_failures() -> None:
    """A crashing check must not prevent others from running."""

    @registry.register("good")
    def good() -> list[Finding]:
        return [_finding("good")]

    @registry.register("bad")
    def bad() -> list[Finding]:
        raise RuntimeError("nope")

    results = {r.check: r for r in run_checks(["good", "bad"])}
    assert results["good"].ok is True
    assert len(results["good"].findings) == 1
    assert results["bad"].ok is False
    assert results["bad"].error is not None
