# -*- coding: utf-8 -*-
import argparse


class cmdparser():
    def __init__(self):

        parent_parser = argparse.ArgumentParser(add_help=False)
        self.parser = argparse.ArgumentParser(add_help=True)

        subparsers = self.parser.add_subparsers(dest="command")
        self.parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.1')
        self.parser.add_argument('-L', '--log', default='info', choices=['all', 'info', 'warning', 'error'], help='list servers, storage, or both (default: %(default)s)')
        self.parser.add_argument('-D', '--dir', type=str)


        # ---------------------------------------------------------------------
        # Master commands
        # ---------------------------------------------------------------------

        # subcommand `check`
        subcmd_check = subparsers.add_parser('check', parents = [parent_parser], help='')


        # ---------------------------------------------------------------------
        # Flow commands
        # ---------------------------------------------------------------------

        # subcommand `config`
        subcmd_config = subparsers.add_parser('config', parents = [parent_parser], help='')
        subcmd_config.add_argument('-D',  '--debug', action='store_true')
        subcmd_config.add_argument('-BS', '--buildsystem',  choices=['ninja', 'msbuild', 'xcode', 'makefiles'])
        subcmd_config.add_argument('-C',  '--compiler',  choices=['gcc', 'clang', 'vc2017', 'vc2019', 'vc2022'])

        # subcommand `lint`
        subcmd_lint = subparsers.add_parser('lint', parents = [parent_parser], help='')
        subcmd_lint.add_argument('-CT', '--clangtidy', action='store_true')
        subcmd_lint.add_argument('-CF', '--clangformat', action='store_true')

        # subcommand `build`
        subcmd_build = subparsers.add_parser('build', parents = [parent_parser], help='')
        subcmd_build.add_argument('-D',  '--debug', action='store_true')
        subcmd_build.add_argument('-BS', '--buildsystem',  choices=['ninja', 'msbuild', 'xcode', 'makefiles'])
        subcmd_build.add_argument('-C',  '--compiler',  choices=['gcc', 'clang', 'vc2017', 'vc2019', 'vc2022'])

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
