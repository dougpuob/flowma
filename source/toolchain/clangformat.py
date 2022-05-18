# -*- coding: utf-8 -*-
import os
import json

from ..lib.execute import process, result


class clangformat():
    _BIN_FILE: str

    # input arguments
    style: str
    inplace: bool

    # objects
    proc: process

    # variables
    probe_success: bool
    probe_except: result
    envdata: json

    def __init__(self,
                 style: str = 'file',
                 inplace: bool = True):

        self.style = style
        self.inplace = inplace

        self._BIN_FILE = 'clang-format'
        self.proc = process()

        self.envdata = os.environ
        retrs: result = self.probe()
        self.probe_success = (0 == retrs.errcode)

        self.probe_except = result()
        self.probe_except.errcode = 9999999
        self.probe_except.stderr.append('exception: clang-format not found !!!')

    def probe(self) -> result:
        argument = ['--version']
        retrs: result = self.proc.exec(self._BIN_FILE,
                                       argument,
                                       env=self.envdata)
        return retrs

    def run(self, file_path: str):
        if not self.probe_success:
            return self.probe_except

        return self.run_v12(file_path)

    def run_v12(self, file_path: str):
        argument = []

        # Change in-place
        if self.inplace:
            argument.append('-i')

        # specific a style
        argument.append('-style={}'.format(self.style))

        argument.append('{}'.format(file_path))

        retrs: result = self.proc.exec('clang-format',
                                       argument,
                                       env=self.envdata)
        return retrs

    def run_v13(self, file_path: str):
        pass

    def run_v14(self, file_path: str):
        pass
