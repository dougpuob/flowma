# -*- coding: utf-8 -*-
import os
import re

from ..lib.execute import process, result


class clangtidy():
    style: str
    inplace: bool

    proc: process

    _BINFILE_: str
    _EXT_NAMES_: list

    def __init__(self,
                 style: str = 'file',
                 inplace: bool = True):

        self.style = style
        self.inplace = inplace

        self.proc = process()

        self._BINFILE_ = 'clang-tidy'
        self._EXT_NAMES_ = ['.c', '.cpp', '.cxx', '.m', '.mm']
        self.envdata = os.environ

    def probe(self) -> result:
        argument = ['--version']
        retrs: result = self.proc.exec(self._BINFILE_,
                                       argument,
                                       env=self.envdata)
        return retrs

    # [PSCustomObject] RunWithJsonCompilationDatabase(
        # [string]$StartDirPath,
        # [bool]$Recursive,
        # [bool]$TryToFix) {

    def run_compilation_database_json(self,
            dir_path: str,
            compile_commands_json_path: str,
            recurse: bool = False,
            fix: bool = False):
        return result()


    def run(self,
            dir_path: str,
            recurse: bool = False,
            fix: bool = False):
        return result()


class clangtidy_assertion():

    raw_text: str
    file_path: str
    line_number: int
    column_number: int
    error_message: str
    error_identifier: str
    failure_message: str

    def parse_assertion(self, raw_text: str):
        pattern = r'([:\\\w\/\.\-\ ]+):(\d+):(\d+): (.+) (\[[\w\-,\.]+\])'
        m = re.match(pattern, raw_text)
        return m

    def __init__(self,
                 assertion_message_block: str,
                 faliure_message: str):

        result = self.parse_assertion(assertion_message_block)
        if 6 == len(result.regs):
            self.raw_text = result[0]
            self.file_path = result[1]
            self.line_number = int(result[2])
            self.column_number = int(result[3])
            self.error_message = result[4]
            self.error_identifier = result[5]
            self.failure_message = faliure_message
