# -*- coding: utf-8 -*-

import os
import logging

from source.lib.define import msvc_edition, msvc_version, os_helper, os_kind
from source.flowma.cmdparser import command_parser
from source.toolchain.msbuild import msvc_information, msbuild
from source.lib.log import logger_format
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

    logfmt = logger_format()
    logfmt.initialize()

    logging.info(logfmt.blue('information') + 'asdfsdafadf')
    logging.warning('warning.................')
    logging.error('error.................')

    hellocamke_projroot = os.path.join(os.getcwd(), r'test/testdata/hello-cmake')
    hellocamke_builddir = os.path.join(os.getcwd(), r'test/testdata/hello-cmake/build')

    envdata = None

    logging.disable()

    if os_helper().is_windows():
        msbld = msbuild()
        supported_msvc_list = msbld.get_supported()
        for msvc_info in supported_msvc_list:
            msvc_info: msvc_information = msvc_info
            msvc_title = logfmt.blue('[MSVC]------------------------------')
            msvc_ver = logfmt.blue('msvc_version')
            msvc_edi = logfmt.blue('msvc_edition')
            vcvarlen = logfmt.blue('vcvars_count')
            logging.info(msvc_title)
            logging.info(' ' + msvc_ver + '={}'.format(msvc_info.version))
            logging.info(' ' + msvc_edi + '={}'.format(msvc_info.edition))
            envdata = msbld.dump_vcvars(msvc_info.edition,
                                        msvc_info.version)
            logging.info(' ' + vcvarlen + '={}'.format(len(envdata)))

    logging.disable(logging.NOTSET)

    proc: process = process()
    retrs: result = proc.exec('cmake',
                              ['-G', 'Ninja',
                               '-B', hellocamke_builddir],
                              workdir=hellocamke_projroot)

    retrs: result = proc.exec('cmake',
                              ['--build', hellocamke_builddir],
                              workdir=hellocamke_projroot)
    print('')

    # vcvars_json = msbld.dump_vcvars(msvc_edition.community,
    #                                 msvc_version.vs2022)

    print('')
