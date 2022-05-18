# -*- coding: utf-8 -*-
import os
import json

from ..lib.execute import process, result
from ..lib.define import build_system, build_compiler, os_helper, os_kind
from ..lib.define import msvc_edition, msvc_version


class flowma_lint():

    envdata: json = {}
    proc: process

    def __init__(self):
        self.envdata = os.environ
        self.proc = process()

    def probe_clangfmt(self) -> result:
        binfile = 'clang-format'
        argument = ['--version']
        retrs: result = self.proc.exec(binfile,
                                       argument,
                                       env=self.envdata)
        return retrs

    def _probe_clangtidy(self) -> result:
        binfile = 'clang-tidy'
        argument = ['--version']
        retrs: result = self.proc.exec(binfile,
                                       argument,
                                       env=self.envdata)
        return retrs

    def probe(self) -> result:

        # clang-format
        retrs: result = self.probe_clangfmt()
        if 0 != retrs.errcode:
            return retrs

        # clang-tidy
        retrs: result = self._probe_clangtidy()
        if 0 != retrs.errcode:
            return retrs

    def clangformat(self,
                    file_path: str,
                    style: str = 'file',
                    inplace: bool = True):
        return self.clangformat_v12(file_path, style, inplace)

    def clangformat_v12(self,
                        file_path: str,
                        style: str = 'file',
                        inplace: bool = True):

        retrs: result = self.probe_clangfmt()
        if 0 != retrs.errcode:
            return retrs

        argument = []

        # Change in-place
        if inplace:
            argument.append('-i')

        # specific a style
        argument.append('-style={}'.format(style))

        argument.append('{}'.format(file_path))

        retrs: result = self.proc.exec('clang-format',
                                       argument,
                                       env=self.envdata)
        return retrs

    def clangformat_v13(self,
                        file_path: str,
                        style: str = 'file',
                        inplace: bool = True):
        pass

    def clangformat_v14(self,
                        file_path: str,
                        style: str = 'file',
                        inplace: bool = True):
        pass

    def clangtidy(self):
        retrs: result = self._probe_clangtidy()
        if 0 != retrs.errcode:
            return retrs

