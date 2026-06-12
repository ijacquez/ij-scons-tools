"""Tests for this SCons Tool module."""

from __future__ import annotations

from typing import Any

from ij_scons_tools.site_tools import pkg_config


class FakeEnvironment(dict[str, Any]):
    """Minimal SCons-like construction environment for Tool smoke tests."""

    def __init__(self) -> None:
        super().__init__()
        self.added_methods: dict[str, Any] = {}

    def SetDefault(self, **kwargs: Any) -> None:  # noqa: N802 - SCons API name.
        """Implement the SCons ``SetDefault`` behavior needed by this test."""
        for key, value in kwargs.items():
            self.setdefault(key, value)

    def AddMethod(self, method: Any, name: str) -> None:  # noqa: N802 - SCons API name.
        """Record methods that a Tool adds to the construction environment."""
        self.added_methods[name] = method


def test_generate_registers_method_and_defaults() -> None:
    """The Tool registers its method and default construction variable."""
    env = FakeEnvironment()

    pkg_config.generate(env)

    assert "PkgConfigGetLibs" in env.added_methods
    assert "PkgConfigGetStaticLibs" in env.added_methods
    assert "PkgConfigGetCFlags" in env.added_methods
    assert "PkgConfigGetAllFlags" in env.added_methods


def test_exists_returns_true() -> None:
    """The "pkg_config" Tool has an external executable (pkg-config) to probe."""
    assert pkg_config.exists(FakeEnvironment()) is True
