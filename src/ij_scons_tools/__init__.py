"""Package metadata for the PIP-distributed SCons Tools."""

from __future__ import annotations

from typing import Final

__all__ = (
    "SITE_TOOLS_MODULE",
    "__version__",
)

__version__: Final[str] = "0.3.1"
SITE_TOOLS_MODULE: Final[str] = "ij_scons_tools.pkg_config"
