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

from pathlib import Path
from typing import Any, Dict, List, Mapping

from SCons.Action import Action
from SCons.Builder import Builder
from SCons.Environment import Environment


def _render_template(path: Path, substitutions: Mapping[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in substitutions.items():
        text = text.replace("@{}@".format(key), value)
    return text


def _action(target: List[Any], source: List[Any], env: Environment, **kw) -> None:
    template: Path = Path(str(source[0]))
    target_path: Path = Path(target[0].path)
    target_name: str = (
        env["PKG_CONFIG_PC_NAME"]
        if env["PKG_CONFIG_PC_NAME"] is not None
        else target_path.stem
    )
    substitutions: Dict[str, str] = {
        "NAME": target_name,
        "DESCRIPTION": env["PKG_CONFIG_PC_DESCRIPTION"],
        "VERSION": env["PKG_CONFIG_PC_VERSION"],
        "prefix": env["PKG_CONFIG_PC_PREFIX"],
        "libdir": env["PKG_CONFIG_PC_LIBDIR"],
        "includedir": env["PKG_CONFIG_PC_INCLUDEDIR"],
    }
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(_render_template(template, substitutions), encoding="utf-8")


def _emitter(target, source, env: Environment):
    """Fix up the source/targets."""
    return target, source


def generate(env: Environment, **kwargs) -> None:
    env.SetDefault(PKG_CONFIG_PC_COMSTR="Building pkg-config $TARGET")
    env.SetDefault(PKG_CONFIG_PC_NAME="Unnamed")
    env.SetDefault(PKG_CONFIG_PC_DESCRIPTION="Description goes here.")
    env.SetDefault(PKG_CONFIG_PC_VERSION="1.0.0")
    env.SetDefault(PKG_CONFIG_PC_PREFIX="usr")
    env.SetDefault(PKG_CONFIG_PC_LIBDIR="lib")
    env.SetDefault(PKG_CONFIG_PC_INCLUDEDIR="include")

    env["BUILDERS"]["PkgConfigPCFile"] = Builder(
        action=Action(_action, "$PKG_CONFIG_PC_COMSTR"),
        emitter=_emitter,
        suffix="pc",
    )


def exists(env: Environment) -> bool:
    return True


# Local Variables:
# coding: utf-8
# End:
