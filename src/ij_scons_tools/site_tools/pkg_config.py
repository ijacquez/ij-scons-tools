"""A SCons tool to simplify pkg-config usage."""

# Copyright (c) 2015 Naranjo Manuel Francisco
# Copyright (c) 2026 Israel Jacquez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from functools import partial
from typing import Dict, List, Optional

from SCons.Environment import Environment
from SCons.SConf import CheckContext

_StrListDict = Dict[str, List[str]]


def _parse_flags(out: _StrListDict, env: Environment, command: str, _: bool) -> None:
    out.update(env.ParseFlags(command))


def PkgConfigSupported(chk_ctx: CheckContext, version: Optional[str] = None) -> bool:
    version_value = (
        version if version is not None else chk_ctx.env["PKG_CONFIG_MIN_VERSION"]
    )
    chk_ctx.Message(
        chk_ctx.env.subst(
            f"Checking for ${{PKG_CONFIG_BIN}} with version >= {version_value}..."
        )
    )
    return_code, _ = chk_ctx.TryAction(
        chk_ctx.env.subst(
            f"${{PKG_CONFIG_BIN}} --atleast-pkgconfig-version={version_value}"
        )
    )
    chk_ctx.Result(return_code == 1)
    return return_code == 1


def PkgConfigCheck(chk_ctx: CheckContext, name: str) -> bool:
    chk_ctx.Message(f"Checking for {name}...")
    return_code, _ = chk_ctx.TryAction(
        chk_ctx.env.subst(
            f"env ${{PKG_CONFIG_BIN}} --with-path '${{PKG_CONFIG_PATH}}' --libs '{name}'"
        )
    )
    chk_ctx.Result(return_code == 1)
    return return_code == 1


def PkgConfigGetLibs(
    env: Environment, name: str, modifyenv: bool = True
) -> _StrListDict:
    env_vars: _StrListDict = {}
    env.ParseConfig(
        env.subst(
            f"${{PKG_CONFIG_BIN}} --with-path '${{PKG_CONFIG_PATH}}' --libs '{name}'"
        ),
        partial(_parse_flags, env_vars),
    )
    if modifyenv:
        env.AppendUnique(**env_vars)
    return env_vars


def PkgConfigGetStaticLibs(
    env: Environment, name: str, modifyenv: bool = True
) -> _StrListDict:
    env_vars: _StrListDict = {}
    env.ParseConfig(
        env.subst(
            f"${{PKG_CONFIG_BIN}} --with-path '${{PKG_CONFIG_PATH}}' --static --libs '{name}'"
        ),
        partial(_parse_flags, env_vars),
    )
    if modifyenv:
        env.AppendUnique(**env_vars)
    return env_vars


def PkgConfigGetCflags(
    env: Environment, name: str, modifyenv: bool = True
) -> _StrListDict:
    env_vars: _StrListDict = {}
    env.ParseConfig(
        env.subst(
            f"${{PKG_CONFIG_BIN}} --with-path '${{PKG_CONFIG_PATH}}' --cflags '{name}'"
        ),
        partial(_parse_flags, env_vars),
    )
    if modifyenv:
        env.AppendUnique(**env_vars)
    return env_vars


def PkgConfigGetAllFlags(env: Environment, name: str, modifyenv: bool = True):
    env_vars: _StrListDict = {}
    env.ParseConfig(
        env.subst(
            f"${{PKG_CONFIG_BIN}} --with-path '${{PKG_CONFIG_PATH}}' --cflags --libs '{name}'"
        ),
        partial(_parse_flags, env_vars),
    )
    if modifyenv:
        env.AppendUnique(**env_vars)
    return env_vars


def generate(env: Environment, **kwargs) -> None:
    from SCons import SConf
    from SCons.SConf import SConfBase

    env.SetDefault(PKG_CONFIG_BIN=env.Detect("pkg-config"))
    env.SetDefault(PKG_CONFIG_PATH=os.getenv("PKG_CONFIG_PATH", ""))
    env.SetDefault(PKG_CONFIG_MIN_VERSION="1.8.0")

    class PkgSConfBase(SConfBase):
        def __init__(self, env: Environment, custom_tests={}, *a, **kw):
            SConfBase.__init__(
                self,
                env,
                {
                    "PkgConfigSupported": PkgConfigSupported,
                    "PkgConfigCheck": PkgConfigCheck,
                }
                | custom_tests,
                *a,
                **kw,
            )

    setattr(SConf, "SConfBase", PkgSConfBase)
    env.AddMethod(PkgConfigGetLibs)
    env.AddMethod(PkgConfigGetStaticLibs)
    env.AddMethod(PkgConfigGetCflags)
    env.AddMethod(PkgConfigGetAllFlags)


def exists(env: Environment) -> bool:
    return env.WhereIs("${PKG_CONFIG_BIN}") is not None


# Local Variables:
# coding: utf-8
# End:
