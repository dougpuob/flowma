# -*- coding: utf-8 -*-
import os
import json

from ..lib.define import msvc_edition, msvc_version, config
from ..lib.path import osdp_path
from ..lib.log import logger_format
from ..lib.log import logger
from ..lib.execute import process, result


class msvc_information():
    version: msvc_version
    edition: msvc_edition
    rootdir: str
    vcvars_files: list

    def __init__(self, ver, edi, rootdir) -> None:
        self.version = ver,
        self.edition = edi
        self.rootdir = rootdir
        self.vcvars_files = []


class vcvars():
    msvc_list_default = []
    msvc_list_customized = []
    logger = None
    logfmt: logger_format
    exec: process

    def __init__(self) -> None:
        self.logfmt = logger_format()
        self.exec = process()

        #
        # Visual Studio 2022
        #
        # C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\vsdevcmd\ext\vcvars.bat
        # C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\vsdevcmd\ext\vcvars\vcvars140.bat
        # C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars32.bat
        # C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat
        # C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat
        # C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsamd64_x86.bat
        # C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsx86_amd64.bat
        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2022,
                msvc_edition.enterprise,
                r'C:\Program Files\Microsoft Visual Studio\2022\BuildTools'))

        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2022,
                msvc_edition.community,
                r'C:\Program Files\Microsoft Visual Studio\2022\Community'))

        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2022,
                msvc_edition.professional,
                r'C:\Program Files\Microsoft Visual Studio\2022\Professional'))

        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2022,
                msvc_edition.enterprise,
                r'C:\Program Files\Microsoft Visual Studio\2022\Enterprise'))

        # vs2019
        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2019,
                msvc_edition.enterprise,
                r'C:\Program Files\Microsoft Visual Studio\2019\BuildTools'))

        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2019,
                msvc_edition.community,
                r'C:\Program Files\Microsoft Visual Studio\2019\Community'))

        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2019,
                msvc_edition.professional,
                r'C:\Program Files\Microsoft Visual Studio\2019\Professional'))

        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2019,
                msvc_edition.enterprise,
                r'C:\Program Files\Microsoft Visual Studio\2019\Enterprise'))

        # vs2017
        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2017,
                msvc_edition.community,
                r'C:\Program Files\Microsoft Visual Studio\2017\Community'))

        self.msvc_list_default.append(
            msvc_information(
                msvc_version.vs2017,
                msvc_edition.professional,
                r'C:\Program Files\Microsoft Visual Studio\2017\Professional'))

        self.msvc_list_default.append(
            msvc_information
            (msvc_version.vs2017,
             msvc_edition.enterprise,
             r'C:\Program Files\Microsoft Visual Studio\2017\Enterprise'))

        self._find_default_vcvars()
        self._find_msvc()

    def find_vcvars(self,
                    msvc_ver: msvc_version = msvc_version.vs2019,
                    msvc_edi: msvc_edition = msvc_edition.community) -> int:

        for item in self.msvc_list_default:
            item: msvc_information = item
            if msvc_edi == item.edition or\
               msvc_ver == item.version:
                return item
        return None

    def add_msvc_info(self, new_msvc_info: msvc_information) -> int:
        self.msvc_list_customized.append(new_msvc_info)

    def _find_msvc(self):
        vswhere_loc = r'C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe'
        retrs: result = self.exec.run(vswhere_loc, ['-format', 'json'])
        if 0 == retrs.errcode:
            data = str(' '.join(retrs.stdout))
            dataobj = config().toCLASS(data)
            for item in dataobj:
                textfmt = self.logfmt.blue('installationPath')
                logger.info(textfmt + '={0}'.format(item.installationPath))

                textfmt = self.logfmt.blue('productLineVersion')
                logger.info(textfmt + '={0}'.format(item.catalog.productLineVersion))

                textfmt = self.logfmt.blue('buildVersion')
                logger.info(textfmt + '={0}'.format(item.catalog.buildVersion))

                textfmt = self.logfmt.blue('displayName')
                logger.info(textfmt + '={0}'.format(item.displayName))

                textfmt = self.logfmt.blue('productPath')
                logger.info(textfmt + '={0}'.format(item.productPath))


    def _find_customized_vcvars(self) -> int:
        self._find_vcvars(self.msvc_list_customized)

    def _find_default_vcvars(self) -> int:
        self._find_vcvars(self.msvc_list_default)

    def _find_vcvars(self, msvc_info_list: list):
        found_count: int = 0

        subdir1 = r'Common7\Tools\vsdevcmd\ext'
        subdir2 = r'VC\Auxiliary\Build'

        path = osdp_path()

        for item in msvc_info_list:
            item: msvc_information = item
            item.vcvars_files.clear()

            path1 = os.path.join(item.rootdir, subdir1)
            path2 = os.path.join(item.rootdir, subdir2)

            if path.exist(path1):
                file_list1 = path.explore_dir(path1, ['.bat'], 'vcvar')
                item.vcvars_files.extend(file_list1)
                found_count += len(item.vcvars_files)
                for vcvar_file in file_list1:
                    file_field = self.logfmt.blue('File')
                    logger.info(file_field + '={0}'.format(vcvar_file))

            if path.exist(path2):
                file_list2 = path.explore_dir(path2, ['.bat'], 'vcvar')
                item.vcvars_files.extend(file_list2)
                found_count += len(item.vcvars_files)

        return found_count

