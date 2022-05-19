# -*- coding: utf-8 -*-
import os
import json

from ..lib.define import os_helper, os_kind
from ..lib.execute import process, result


class clangformat():
    _BIN_FILE: str

    # input arguments
    config_file: str
    style: str
    inplace: bool

    # objects
    _obj_proc: process
    _obj_os_helper: os_helper

    # variables
    oskind: os_kind
    probe_success: bool
    probe_except: result
    envdata: json

    def __init__(self,
                 config_file: str,
                 style: str = 'file',
                 inplace: bool = True,
                 version: int = 0):

        # arguments
        self.config_file = config_file
        self.style = style
        self.inplace = inplace
        self.version = version

        # objects
        self._obj_proc = process()
        self._obj_os_helper = os_helper()

        # definitions
        self.oskind = self._obj_os_helper.get_oskind()
        self._BIN_FILE = 'clang-format'
        if 0 != version:
            if self._obj_os_helper.is_linux(self.oskind) or \
               self._obj_os_helper.is_macos(self.oskind):
                self._BINFILE_ = 'clang-format' + '-' + str(version)

        # others
        self.envdata = os.environ
        retrs: result = self.probe()
        self.probe_success = (0 == retrs.errcode)

        self.probe_except = result()
        self.probe_except.errcode = 9999999
        self.probe_except.stderr.append('exception: clang-format not found !!!')

    def probe(self) -> result:
        argument = ['--version']
        retrs: result = self._obj_proc.exec(self._BIN_FILE,
                                            argument,
                                            env=self.envdata)
        return retrs

    def run(self, source_file_path: str):
        ret = None
        if not self.probe_success:
            ret = self.probe_except
        if 12 == self.version:
            ret = self.run_v12(source_file_path)
        elif 13 == self.version:
            ret = self.run_v13(source_file_path)
        elif 14 >= self.version:
            ret = self.run_v14(source_file_path)
        return ret

    def run_v12(self, source_file_path: str):
        argument = []

        # Change in-place
        if self.inplace:
            argument.append('-i')

        # specific a style
        if 'file' == self.style:
            argument.append('-style=file')
        else:
            argument.append('-style={}'.format(self.style))

        argument.append('{}'.format(source_file_path))

        retrs: result = self._obj_proc.exec(self._BIN_FILE,
                                            argument,
                                            env=self.envdata)
        return retrs

    def run_v13(self, file_path: str):
        return self.run_v12(file_path)

    def run_v14(self, source_file_path: str):
        # -style=file:<format_file_path>
        argument = []

        # Change in-place
        if self.inplace:
            argument.append('-i')

        # specific style and config
        if 'file' == self.style:
            if os.path.exists(self.config_file):
                argument.append('-style=file:{}'.format(self.config_file))
        else:
            argument.append('-style={}'.format(self.style))

        argument.append('{}'.format(source_file_path))

        retrs: result = self._obj_proc.exec(self._BIN_FILE,
                                            argument,
                                            env=self.envdata)
        return retrs
        pass
