# -*- coding: utf-8 -*-
import argparse


class cmdparser():
    def __init__(self):
        #
        # Program arugments
        #
        parent_parser = argparse.ArgumentParser(add_help=False)
        self.parser = argparse.ArgumentParser(add_help=True)

        # create sub-parser
        subparsers = self.parser.add_subparsers(dest="command")
        self.parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.1')
        self.parser.add_argument('-L', '--log', default='all', choices=['all', 'info', 'warning', 'error'], help='list servers, storage, or both (default: %(default)s)')

        # subcommand `config`
        subcmd_config = subparsers.add_parser('config', parents = [parent_parser], help='')

        # subcommand `lint`
        subcmd_lint = subparsers.add_parser('lint', parents = [parent_parser], help='')

        # subcommand `build`
        subcmd_build = subparsers.add_parser('build', parents = [parent_parser], help='')

        # subcommand `pack`
        subcmd_pack = subparsers.add_parser('pack', parents = [parent_parser], help='')

        # subcommand `test`
        subcmd_test = subparsers.add_parser('test', parents = [parent_parser], help='')

        # subcommand `score`
        subcmd_score = subparsers.add_parser('score', parents = [parent_parser], help='')

        # subcommand `upload`
        subcmd_upload = subparsers.add_parser('upload', parents = [parent_parser], help='')


    def print_help(self):
        args = self.parser.print_help()
        return args


    def get_parsed_args(self):
        args = self.parser.parse_args()
        return args
