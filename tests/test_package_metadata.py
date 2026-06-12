"""Tests for public package metadata."""

from __future__ import annotations

import ij_scons_tools


def test_site_tools_module_name_is_stable() -> None:
    """The documented SCons PyPackageDir module name must remain stable."""
    assert ij_scons_tools.SITE_TOOLS_MODULE == "ij_scons_tools.site_tools"


def test_version_is_declared() -> None:
    """The runtime package exposes a non-empty version string."""
    assert ij_scons_tools.__version__
