# -*- coding: utf-8 -*-

from ..lib.execute import process, result


class cmake():
    proc: process

    def __init__(self):
        self.proc = process()
