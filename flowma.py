# -*- coding: utf-8 -*-

from source.lib.define import msvc_edition, msvc_version
from source.flowma.cmdparser import command_parser
from source.toolchain.msbuild import msvc_information, msvc_vcvars
from source.lib.log import logger_format
from source.lib.log import logger


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

    flowma().main()

    cmzfmt = logger_format()

    logger.info(cmzfmt.blue('information') + 'asdfsdafadf')
    logger.warning('warning.................')
    logger.error('error.................')

    vcvar = msvc_vcvars()
    for msvc in vcvar.msvc_info_list:
        msvc: msvc_information = msvc
        for jsondata in msvc.vcvars_jsons:
            logger.info('-------------------------------------------------------------------')
            logger.info(jsondata)

    print('')
