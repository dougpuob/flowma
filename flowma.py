# -*- coding: utf-8 -*-

import logging
import json
import datetime
import os

from src.cmdparser import cmdparser


class flowma():

    def __init__(self):
        self.cmd = cmdparser()
        self.args = cmd.get_parsed_args()

        # logger = logging.getLogger()
        # logger.setLevel(logging.INFO)
        # formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s',
        # 	                            datefmt='%Y%m%d %H:%M:%S')
        # screen = logging.StreamHandler()
        # screen.setLevel(logging.INFO)
        # screen.setFormatter(formatter)

        # logdir='data/log'
        # if not os.path.exists(logdir):
        #     os.makedirs(logdir)

        # filename = datetime.datetime.now().strftime("qemu-tasker--%Y%m%d_%H%M%S.log")
        # logfile = logging.FileHandler(os.path.join(logdir, filename))
        # logfile.setLevel(logging.INFO)
        # logfile.setFormatter(formatter)

        # logger.addHandler(logfile)
        # socket_addr = config_next.socket_address(args.host, args.port)


    def main():
        if 'config' == args.command:
            pass


        elif 'lint' == args.command:
            pass


        elif 'build' == args.command:
            pass


        elif 'pack' == args.command:
            pass


        elif 'score' == args.command:
            pass


        elif 'upload' == args.command:
            pass


        else:
            cmdarg.print_help()



if __name__ == '__main__':
    flowma.main()
