# -*- coding: utf-8 -*-
import os

from ..lib.execute import process, result


class clangtidy():
    style: str
    inplace: bool

    proc: process

    _BINFILE_: str

    def __init__(self,
                 style: str = 'file',
                 inplace: bool = True):

        self.style = style
        self.inplace = inplace

        self.proc = process()

        self._BINFILE_ = 'clang-tidy'
        self.envdata = os.environ

    def probe(self) -> result:
        argument = ['--version']
        retrs: result = self.proc.exec(self._BINFILE_,
                                       argument,
                                       env=self.envdata)
        return retrs

    def run(self, file_path: str):
        return result()


class clangtidy_assertion():

    raw_text: str
    file_path: str
    line_number: int
    column_number: int
    error_message: str
    error_identifier: str
    failure_message: str

    def __init__(self,
                 assertion_message_block: str,
                 faliure_message: str):

        self.raw_text = ''
        self.file_path = ''
        self.line_number = 0
        self.column_number = 0
        self.error_message = ''
        self.error_identifier = ''
        self.failure_message = faliure_message
