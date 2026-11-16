"""Core data structures for penguin-audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    """How bad a finding is, lowest to highest."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Finding:
    """One observation produced by a check.

    Findings are immutable snapshots of observed state — once created, they
    must not be modified, or baseline diffing (M3) compares apples to edited apples.
    """

    check: str
    code: str
    severity: Severity
    title: str
    description: str
    evidence: dict[str, Any] = field(default_factory=dict)
    remediation: str = ""
    references: tuple[str, ...] = ()


@dataclass
class CheckResult:
    """The result of running one check.

    Produced by the runner — checks themselves don't see this; they only see
    how to emit Finding objects (or return them, depending on the decision).
    """

    check: str
    findings: list[Finding] = field(default_factory=list)
    duration_ms: float = 0.0
    error: str | None = None
    traceback: str = ""

    @property
    def ok(self) -> bool:
        """True if the check ran without an exception."""
        return self.error is None
