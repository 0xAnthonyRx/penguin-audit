"""Tests for the check registry."""

import pytest

from penguin_audit.core import registry
from penguin_audit.core.models import Finding


@pytest.fixture(autouse=True)
def clean_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each test gets a fresh empty registry so tests don't leak into each other."""
    monkeypatch.setattr(registry, "_REGISTRY", {})


def test_register_and_get() -> None:
    @registry.register("fake")
    def fake() -> list[Finding]:
        return []

    assert registry.get_check("fake") is fake


def test_register_duplicate_raises() -> None:
    @registry.register("fake")
    def fake1() -> list[Finding]:
        return []

    with pytest.raises(ValueError, match="already registered"):

        @registry.register("fake")
        def fake2() -> list[Finding]:
            return []


def test_get_unknown_raises_keyerror() -> None:
    with pytest.raises(KeyError, match="nope"):
        registry.get_check("nope")


def test_list_checks_is_sorted() -> None:
    @registry.register("bbb")
    def b() -> list[Finding]:
        return []

    @registry.register("aaa")
    def a() -> list[Finding]:
        return []

    assert registry.list_checks() == ["aaa", "bbb"]


def test_all_checks_returns_a_copy() -> None:
    @registry.register("x")
    def x() -> list[Finding]:
        return []

    snapshot = registry.all_checks()
    snapshot["hacked"] = x  # mutating the returned dict
    assert "hacked" not in registry.list_checks()  # internal state unchanged
