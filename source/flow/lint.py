# -*- coding: utf-8 -*-
import os
import json

from source.toolchain.clangformat import clangformat
from source.toolchain.clangtidy import clangtidy

from ..lib.execute import process, result
from ..lib.define import build_system, build_compiler, os_helper, os_kind
from ..lib.define import msvc_edition, msvc_version


class flowma_lint():

    clangfmt_obj: clangformat
    clangtidy_obj: clangtidy

    def __init__(self):
        self.proc = process()
        self.clangfmt_obj = clangformat()
        self.clangtidy_obj = clangtidy()

    def probe(self) -> result:

        # clang-format
        retrs: result = self.clangfmt_obj.probe()
        if 0 != retrs.errcode:
            return retrs

        # clang-tidy
        retrs: result = self.clangtidy_obj.probe()
        if 0 != retrs.errcode:
            return retrs

        return result()

    def clangformat(self, file: str):
        return self.clangfmt_obj.run(file)

    def clangtidy(self, file: str):
        return self.clangtidy_obj.run(file)
