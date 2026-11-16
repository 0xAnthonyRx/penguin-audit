"""Registry: maps check names to their implementing functions.

Checks announce themselves with @register("name"). The runner, CLI, and tests
all use this module to discover what checks exist.
"""

from __future__ import annotations

from collections.abc import Callable

from penguin_audit.core.models import Finding

# A check is a zero-argument function that returns a list of findings.
CheckFunc = Callable[[], list[Finding]]

# Module-private: don't touch from outside. Use the functions below.
_REGISTRY: dict[str, CheckFunc] = {}


def register(name: str) -> Callable[[CheckFunc], CheckFunc]:
    """Decorator: register a function as the check named `name`.

    Raises ValueError if `name` is already registered — that's a bug, not a
    feature, and we want to catch it at import time, not silently shadow.
    """

    def decorator(func: CheckFunc) -> CheckFunc:
        if name in _REGISTRY:
            raise ValueError(f"Check {name!r} is already registered")
        _REGISTRY[name] = func
        return func

    return decorator


def get_check(name: str) -> CheckFunc:
    """Look up a check by name. Raises KeyError if not found."""
    if name not in _REGISTRY:
        raise KeyError(f"Unknown check: {name!r}")
    return _REGISTRY[name]


def list_checks() -> list[str]:
    """All registered check names, sorted for stable output."""
    return sorted(_REGISTRY)


def all_checks() -> dict[str, CheckFunc]:
    """A copy of the registry — callers can't mutate our internal state."""
    return dict(_REGISTRY)
