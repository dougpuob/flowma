# -*- coding: utf-8 -*-
import os
import json

from source.toolchain.clangformat import clangformat
from source.toolchain.clangtidy import clangtidy

from ..lib.define import CONFIGURATION
from ..lib.execute import process, result
from ..lib.define import build_system, build_compiler, os_helper, os_kind
from ..lib.define import msvc_edition, msvc_version


class lint_config(CONFIGURATION):

    class llvm(CONFIGURATION):

        compile_commands: str = ''
        specific_version: int = 0

        class config(CONFIGURATION):

            clangformat: str = ''
            clangtidy: str = ''


class flowma_lint():

    _obj_proc: process
    _obj_clangfmt: clangformat
    _obj_clangtidy: clangtidy

    compile_commands_json_path: str
    clang_tidy_config_path: str

    # member_variables
    _ver_clangfmt: int
    _ver_clangtdy: int

    def __init__(self, config: lint_config):

        self._obj_proc = process()
        self._obj_clangfmt = clangformat(config.llvm.config.clangformat,
                                         version=config.llvm.specific_version)
        self._ver_clangfmt = config.llvm.specific_version

        self._obj_clangtidy = clangtidy(config.llvm.compile_commands,
                                        config.llvm.config.clangtidy,
                                        version=config.llvm.specific_version)
        self._ver_clangtdy = config.llvm.specific_version

    def probe(self) -> result:

        # clang-format
        retrs: result = self._obj_clangfmt.probe()
        if 0 != retrs.errcode:
            return retrs

        # clang-tidy
        retrs: result = self._obj_clangtidy.probe()
        if 0 != retrs.errcode:
            return retrs

        return result()

    def check_version(self) -> bool:
        ver_clangfmt = self._obj_clangfmt.get_version()
        ver_clangtdy = self._obj_clangtidy.get_version()

        identical: bool = self._ver_clangfmt == ver_clangfmt[0] and \
            self._ver_clangtdy == ver_clangtdy[0]

        return identical

    def clangformat(self, file: str):
        return self._obj_clangfmt.run(file)

    def clangtidy(self, file: str):
        return self._obj_clangtidy.run(file)
