# -*- coding: utf-8 -*-
import logging
import os
import re
import json

from ..lib.path import osdp_path
from ..lib.define import os_helper, os_kind
from ..lib.execute import process, result


class clangformat():
    _BINFILE_: str

    # input arguments
    config_file: str
    style: str
    inplace: bool

    # objects
    _obj_osdp_path: osdp_path
    _obj_proc: process
    _obj_os_helper: os_helper

    # variables
    oskind: os_kind
    probe_success: bool
    except_probe: result
    envdata: json

    # member variables
    queried_version: list

    def __init__(self,
                 config_file: str,
                 style: str = 'file',
                 inplace: bool = True,
                 version: int = 0):

        # objects
        self._obj_osdp_path = osdp_path()
        self._obj_proc = process()
        self._obj_os_helper = os_helper()

        # arguments
        self.config_file = self._obj_osdp_path.normpath(config_file)
        self.style = style
        self.inplace = inplace
        self.version = version

        # definitions
        self.oskind = self._obj_os_helper.get_oskind()
        self._BINFILE_ = 'clang-format'
        if self._obj_os_helper.is_linux(self.oskind) or \
           self._obj_os_helper.is_macos(self.oskind):
            self._BINFILE_ += '-' + str(version)

        # others
        self.envdata = os.environ
        retrs: result = self.probe()
        self.probe_success = (0 == retrs.errcode)

        self.except_probe = result()
        self.except_probe.errcode = 9999999
        self.except_probe.stderr.append("exception: clang-format not found !!!")

        self.except_version_mismatched = result()
        self.except_version_mismatched.errcode = 9999998
        self.except_version_mismatched.stderr.append("exception: the specific version was found at this system !!!")

        self.except_version_less_than_12 = result()
        self.except_version_less_than_12.errcode = 9999997
        self.except_version_less_than_12.stderr.append("exception: flowma doesn't support version less than 12 !!!")

        # member variables
        self.queried_version = self.get_version()

    def probe(self) -> result:
        argument = ['--version']
        retrs: result = self._obj_proc.exec(self._BINFILE_,
                                            argument,
                                            env=self.envdata)
        return retrs

    def get_version(self) -> list:
        ver_info = [0, 0, 0]
        retrs: result = self.probe()
        if 0 == retrs.errcode:
            # clang-format version 15.0.0
            vers_tuple = re.findall("(\\d+)\\.(\\d+)\\.(\\d+)", ''.join(retrs.stdout))
            ver_info[0] = int(vers_tuple[0][0])
            ver_info[1] = int(vers_tuple[0][1])
            ver_info[2] = int(vers_tuple[0][2])
        return ver_info

    def run(self, source_file_path: str) -> result:
        retrs: result = None

        if not self.probe_success:
            retrs = self.except_probe
            logging.debug('{}'.format(''.join(retrs.stderr)))
            return retrs

        specific_version = 0
        if 0 != self.version:
            specific_version = self.version

        if specific_version != self.queried_version[0]:
            retrs = self.except_version_mismatched
            logging.debug('{}'.format(''.join(retrs.stderr)))

        elif specific_version < 12:
            retrs = self.except_version_less_than_12
            logging.debug('{}'.format(''.join(retrs.stderr)))
        elif 14 >= specific_version:
            retrs = self.run_v14(source_file_path)
        elif 13 == specific_version:
            retrs = self.run_v13(source_file_path)
        elif 12 == specific_version:
            retrs = self.run_v12(source_file_path)
        else:
            retrs = self.run_v14(source_file_path)

        return retrs

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

        retrs: result = self._obj_proc.exec(self._BINFILE_,
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
            argument.append('-style="{}"'.format(self.style))

        argument.append('{}'.format(source_file_path))

        retrs: result = self._obj_proc.exec(self._BINFILE_,
                                            argument,
                                            env=self.envdata)

        logging.info(self._BINFILE_ + ' ' + ' '.join(argument))
        return retrs
