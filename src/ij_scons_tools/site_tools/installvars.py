# Copyright (c) 2026 Israel Jacquez
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import Any

from SCons.Script import Environment, PathVariable, Variables


def _path_variable(name: str, help_text: str, default: str) -> Any:
    return PathVariable(
        name,
        help=help_text,
        default=default,
        validator=PathVariable.PathAccept,
    )


def InstallVariables(
    env: Environment,
    *,
    prefix: str = "/usr",
    includedir: str = "${prefix}/include",
    libdir: str = "${prefix}/lib",
    destdir: str = "",
) -> Any:
    variables = Variables()
    variables.AddVariables(
        _path_variable(
            "prefix",
            "logical installation prefix",
            prefix,
        ),
        _path_variable(
            "includedir",
            "public header installation directory",
            includedir,
        ),
        _path_variable(
            "libdir",
            "library installation directory",
            libdir,
        ),
        _path_variable(
            "DESTDIR",
            "staged installation root; prepended to install targets only",
            destdir,
        ),
    )
    variables.Update(env)
    return variables


def generate(env: Any, **kwargs) -> None:
    env.AddMethod(InstallVariables)


def exists(env: Any) -> bool:
    return True
