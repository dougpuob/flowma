# -*- coding: utf-8 -*-

import os

from source.lib.define import msvc_edition, msvc_version
from source.flowma.cmdparser import command_parser
from source.toolchain.msbuild import msvc_information, msbuild
from source.lib.log import logger_format
from source.lib.log import logger
from source.lib.execute import process, result


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

    proc: process = process()

    msbld = msbuild()
    supported_msvc_list = msbld.get_supported()
    for msvc_info in supported_msvc_list:
        msvc_info: msvc_information = msvc_info
        msvc_title = cmzfmt.blue('[MSVC]------------------------------')
        msvc_ver = cmzfmt.blue('msvc_version')
        msvc_edi = cmzfmt.blue('msvc_edition')
        vcvarlen = cmzfmt.blue('vcvars_count')
        logger.info(msvc_title)
        logger.info(' ' + msvc_ver + '={}'.format(msvc_info.version))
        logger.info(' ' + msvc_edi + '={}'.format(msvc_info.edition))
        vcvars_json = msbld.dump_vcvars(msvc_info.edition,
                                        msvc_info.version)
        logger.info(' ' + vcvarlen + '={}'.format(len(vcvars_json)))
        hellocamke_projroot = os.path.join(os.getcwd(), r'test/testdata/hello-cmake')
        hellocamke_builddir = os.path.join(os.getcwd(), r'test/testdata/hello-cmake/build')
        retrs: result = proc.run('cmake',
                                 ['-G', 'Ninja', '-B', hellocamke_builddir],
                                 workdir=hellocamke_projroot,
                                 env=vcvars_json)
        retrs: result = proc.run('cmake',
                                 ['--build', hellocamke_builddir],
                                 workdir=hellocamke_projroot,
                                 env=vcvars_json)
        print('')

    # vcvars_json = msbld.dump_vcvars(msvc_edition.community,
    #                                 msvc_version.vs2022)

    print('')
