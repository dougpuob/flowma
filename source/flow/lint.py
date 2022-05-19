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

    def __init__(self) -> None:
        pass

    class llvm(CONFIGURATION):

        compile_commands: str

        def __init__(self) -> None:
            pass

        class config(CONFIGURATION):

            clangformat: str
            clangtidy: str

            def __init__(self) -> None:
                pass


class flowma_lint():

    _obj_clangfmt: clangformat
    _obj_clangtidy: clangtidy

    compile_commands_json_path: str
    clang_tidy_config_path: str

    def __init__(self, config: lint_config):

        self.proc = process()
        self._obj_clangfmt = clangformat()
        self._obj_clangtidy = clangtidy(config.llvm.compile_commands,
                                        config.llvm.config.clangtidy)

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

    def clangformat(self, file: str):
        return self._obj_clangfmt.run(file)

    def clangtidy(self, file: str):
        return self._obj_clangtidy.run(file)
