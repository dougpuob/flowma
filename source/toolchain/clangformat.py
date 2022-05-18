# -*- coding: utf-8 -*-

from ..lib.execute import process, result


class clangformat():
    proc: process

    def __init__(self):
        self.proc = process()
