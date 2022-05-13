# -*- coding: utf-8 -*-

import logging

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


    prefix = '[%(asctime)s][%(levelname)s] %(message)s'
    format = logging.Formatter(prefix, datefmt='%H:%M:%S')
    screen = logging.StreamHandler()
    screen.setFormatter(format)
    logger = logging.getLogger()
    logger.addHandler(screen)
    logger.setLevel(logging.INFO)


    flowma().main()


    logger.info('sadfsafdsafsadf')
    logger.error('sadfsafdsafsadf')

