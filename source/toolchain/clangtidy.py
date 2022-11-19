# -*- coding: utf-8 -*-
import os
import re
import json

from ..lib.execute import process, result
from ..lib.define import os_helper, os_kind


class clangtidy_assertion():
    _START_: int
    _END_: int

    raw_text: str = ''
    file_path: str = ''
    line_number: int = 0
    column_number: int = 0
    error_message: str = ''
    error_identifier: str = ''
    failure_message: list = []

class clangtidy_assertion_parser():
    assertion_list: list
    _PATTERN_: str

    def find_assertion_blocks(self, raw_text: str):
        pattern = re.compile(self._PATTERN_, re.MULTILINE)
        m = pattern.findall(raw_text)
        return m

    # def parse_assertion(self, raw_text: str):
    #     m = re.match(self._PATTERN_, raw_text)
    #     return m

    def parse(self, stdout_rawtext: str):
        stdout_rawtext = stdout_rawtext.strip()
        self.assertion_list.clear()

        block_list = self.find_assertion_blocks(stdout_rawtext)

        for block in block_list:
            if 5 == len(block):
                new_assert = clangtidy_assertion()
                new_assert.file_path = block[0]
                new_assert.line_number = int(block[1])
                new_assert.column_number = int(block[2])
                new_assert.error_message = block[3]
                new_assert.error_identifier = block[4]

                start_text = (new_assert.file_path + ':' +
                              str(new_assert.line_number) + ':' +
                              str(new_assert.column_number) + ':')
                new_assert._START_ = stdout_rawtext.find(start_text)
                new_assert._END_ = stdout_rawtext.find(new_assert.error_identifier,
                                                       new_assert._START_)
                if new_assert._END_ != -1:
                    new_assert._END_ += len(new_assert.error_identifier)

                self.assertion_list.append(new_assert)

        next_index = 0
        for assertion in self.assertion_list:
            next_index += 1
            assertion: clangtidy_assertion = assertion
            start_curr: int = assertion._END_
            start_next: int = 0

            if len(self.assertion_list) > next_index:
                start_next = self.assertion_list[next_index]._START_
            else:
                start_next = len(stdout_rawtext)

            failure_text = stdout_rawtext[start_curr:start_next].strip()
            assertion.failure_message = failure_text.split('\n')

        return self.assertion_list

    def __init__(self):
        self.assertion_list = []
        self._PATTERN_ = r'([:\\\w\/\.\-\ ]+):(\d+):(\d+): (.+) (\[[\w\-,\.]+\])'


class clangtidy():

    # definitions
    _BINFILE_: str
    _EXT_NAMES_: list

    # arguments
    compile_commands_json_path: str
    clang_tidy_config_path: str
    style: str
    inplace: bool
    version: int

    # objects
    _obj_proc: process
    _obj_parser: clangtidy_assertion_parser
    _obj_os_helper: os_helper

    # others
    oskind: os_kind
    envdata: json
    lastcmd: list

    # member variables
    queried_version: list

    def __init__(self,
                 clang_tidy_config_path: str,
                 compile_commands_json_path: str = None,
                 style: str = 'file',
                 inplace: bool = False,
                 version: int = 0):

        # objects
        self._obj_os_helper = os_helper()
        self._obj_proc = process()
        self._obj_parser = clangtidy_assertion_parser()

        # arguments
        self.clang_tidy_config_path = clang_tidy_config_path
        self.compile_commands_json_path = compile_commands_json_path
        self.style = style
        self.inplace = inplace

        # definitions
        self._EXT_NAMES_ = ['.c', '.cpp', '.cxx', '.m', '.mm']
        self.oskind = self._obj_os_helper.get_oskind()
        self._BINFILE_ = 'clang-tidy'
        if self._obj_os_helper.is_linux(self.oskind) or \
           self._obj_os_helper.is_macos(self.oskind):
            self._BINFILE_ += '-' + str(version)

        # others
        self.envdata = os.environ
        self.lastcmd = []

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
            # PS > clang-tidy.exe --version
            # LLVM (http://llvm.org/):
            #   LLVM version 15.0.0
            #   Optimized build.
            #   Default target: x86_64-pc-windows-msvc
            #   Host CPU: znver2
            vers_tuple = re.findall("(\\d+)\\.(\\d+)\\.(\\d+)", ''.join(retrs.stdout))
            ver_info[0] = int(vers_tuple[0][0])
            ver_info[1] = int(vers_tuple[0][1])
            ver_info[2] = int(vers_tuple[0][2])
        return ver_info

    def explain_config(self,
                       config: str):

        self.lastcmd.clear()

        arguments: list = []
        arguments.append('--explain-config')

        if os.path.exists(self.compile_commands_json_path):
            arguments.extend(['-p', self.compile_commands_json_path])

        if os.path.exists(config):
            arguments.append('--config-file={}'.format(config))

        # execute this command
        retrs: result = self._obj_proc.exec(self._BINFILE_,
                                            arguments,
                                            env=self.envdata)
        return retrs

    def run(self,
            source_file_path: str,
            config: str,
            fix: bool = False):

        self.lastcmd.clear()

        arguments: list = []

        if os.path.exists(self.compile_commands_json_path):
            arguments.extend(['-p', self.compile_commands_json_path])

        arguments.append(source_file_path)

        if os.path.exists(config):
            arguments.append('--config-file={}'.format(config))
        else:
            arguments.append('--checks="{}"'.format(config))

        if fix:
            arguments.append('-fix')

        # arguments.append('-enable-check-profile')
        # arguments.append('-store-check-profile={}'.format(DIRPATH))

        # execute this command
        retrs: result = self._obj_proc.exec(self._BINFILE_,
                                            arguments,
                                            env=self.envdata)

        retrs.data = self._obj_parser.parse('\n'.join(retrs.stdout))

        # update last command
        self.lastcmd.append(self._BINFILE_)
        self.lastcmd.extend(arguments)

        print(self.lastcmd)

        return retrs
