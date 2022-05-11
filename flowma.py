# -*- coding: utf-8 -*-

import logging
import json
import datetime
import os

from source.flowma.cmdparser import command_parser


class flowma():


    def __init__(self):
        self.cmd_parser = command_parser()
        self.args = self.cmd_parser.get_parsed_args()


    def main(self):
        if 'config' == self.args.command:
            pass


        elif 'lint' == self.args.command:
            pass


        elif 'build' == self.args.command:
            pass


        elif 'pack' == self.args.command:
            pass


        elif 'score' == self.args.command:
            pass


        elif 'upload' == self.args.command:
            pass


        else:
            self.cmd_parser.print_help()


if __name__ == '__main__':
    flowma.main()

