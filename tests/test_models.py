"""Tests for core data models."""

import dataclasses

import pytest

from penguin_audit.core.models import CheckResult, Finding, Severity


def _finding(**overrides: object) -> Finding:
    """Build a minimal valid Finding, override fields per-test."""
    base: dict[str, object] = {
        "check": "test",
        "code": "TEST001",
        "severity": Severity.LOW,
        "title": "t",
        "description": "d",
    }
    base.update(overrides)
    return Finding(**base)  # type: ignore[arg-type]


def test_severity_is_string_valued() -> None:
    """Severity subclasses str, so JSON encoding works out of the box."""
    assert Severity.INFO.value == "info"
    assert Severity.CRITICAL == "critical"  # str comparison works


def test_finding_is_frozen() -> None:
    f = _finding()
    with pytest.raises(dataclasses.FrozenInstanceError):
        f.title = "changed"  # type: ignore[misc]


def test_finding_evidence_is_not_shared_between_instances() -> None:
    a = _finding(check="a")
    b = _finding(check="b")
    assert a.evidence is not b.evidence
    a.evidence["x"] = 1
    assert b.evidence == {}


def test_check_result_defaults() -> None:
    r = CheckResult(check="test")
    assert r.findings == []
    assert r.duration_ms == 0.0
    assert r.error is None
    assert r.ok is True


def test_check_result_with_error_is_not_ok() -> None:
    r = CheckResult(check="test", error="boom")
    assert r.ok is False
