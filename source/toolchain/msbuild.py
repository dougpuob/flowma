# -*- coding: utf-8 -*-

import os
import re
import json

from ..lib.define import cpu_architecture
from ..lib.define import msvc_edition, msvc_version, config
from ..lib.path import osdp_path
from ..lib.log import logger_format
from ..lib.log import logger
from ..lib.execute import process, result


class msvc_information():
    #
    # Official information (vswhere.exe)
    #
    installationPath: str    # C:\Program Files\Microsoft Visual Studio\2022\Community
    productLineVersion: int  # 2022
    buildVersion: str        # 17.1.32210.238
    displayName: str         # Visual Studio Community 2022
    productPath: str         # C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe

    instanceId: str          # f6176bb6
    installDate: str         # 2021-12-03T12:49:31Z
    productId: str           # Microsoft.VisualStudio.Product.Community

    #
    # display name information
    #
    edition: msvc_edition
    version: msvc_version

    subdir_list: list
    vcvars_files: list
    vcvars_jsons: list

    def __init__(self, display_name: str) -> None:
        self.vcvars_files = []
        self.subdir_list = []
        self.vcvars_jsons = []

        self.displayName = display_name.strip()
        display_name = self.displayName.lower()

        if display_name.find('community') >= 0:
            self.edition = msvc_edition.community
        elif display_name.find('buildtools') >= 0:
            self.edition = msvc_edition.buildtools
        elif display_name.find('professional') >= 0:
            self.edition = msvc_edition.professional
        elif display_name.find('enterprise') >= 0:
            self.edition = msvc_edition.enterprise

        if display_name.find('2022') >= 0:
            self.version = msvc_version.vs2022
        elif display_name.find('2019') >= 0:
            self.version = msvc_version.vs2019
        elif display_name.find('2017') >= 0:
            self.version = msvc_version.vs2017
        elif display_name.find('2015') >= 0:
            self.version = msvc_version.vs2015


class msbuild():
    msvc_info_list: list

    _logger = None
    _logfmt: logger_format
    _exec: process
    _path: osdp_path
    _vswhere: str

    def __init__(self) -> None:
        self._logfmt = logger_format()
        self._exec = process()
        self._path = osdp_path()
        self._vswhere = r'C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe'

        msvc_info_list = self._find_msvc()
        self.msvc_info_list = self._find_vcvars(msvc_info_list)

    def get_supported(self):
        return self.msvc_info_list

    def dump_vcvars(self,
                    msvc_edi: msvc_edition,
                    msvc_ver: msvc_version,
                    host_cpu: cpu_architecture = cpu_architecture.x86_64,
                    target_cpu: cpu_architecture = cpu_architecture.x86_64):

        # vcvars32.bat          x86
        # vcvars64.bat          x64
        # vcvarsamd64_x86.bat   x64_x86
        # vcvarsx86_amd64.bat   x86_x64

        vcvarbat = ''
        if (cpu_architecture.x86_32.value == target_cpu.value) and \
           (cpu_architecture.x86_32.value == host_cpu.value):
            vcvarbat = 'vcvars32.bat'
        elif (cpu_architecture.x86_64.value == target_cpu.value) and \
             (cpu_architecture.x86_64.value == host_cpu.value):
            vcvarbat = 'vcvars64.bat'
        elif (cpu_architecture.x86_64.value == host_cpu.value) and \
             (cpu_architecture.x86_32.value == target_cpu.value):
            vcvarbat = 'vcvarsamd64_x86.bat'
        elif (cpu_architecture.x86_32.value == host_cpu.value) and\
             (cpu_architecture.x86_64.value == target_cpu.value):
            vcvarbat = 'vcvarsx86_amd64.bat'
        else:
            vcvarbat = 'vcvars64.bat'

        for msvc_info in self.msvc_info_list:
            msvc_info: msvc_information = msvc_info
            if (msvc_info.edition.value == msvc_edi.value) and \
               (msvc_info.version.value == msvc_ver.value):
                for vcvar_file in msvc_info.vcvars_files:
                    basename = os.path.basename(vcvarbat)
                    if basename == vcvarbat:
                        jsondata = self._dump_vcvars(vcvar_file)
                        return jsondata
        return None

    def _find_msvc(self):
        msvc_info_list: list = []

        retrs: result = self._exec.exec(self._vswhere, ['-format', 'json'])
        if 0 == retrs.errcode:
            data = config().toCLASS(str(' '.join(retrs.stdout)))
            for item in data:
                msvc_info = msvc_information(item.displayName)

                msvc_info.productPath = item.productPath
                msvc_info.displayName = item.displayName
                msvc_info.buildVersion = item.catalog.buildVersion
                msvc_info.productLineVersion = item.catalog.productLineVersion
                msvc_info.installationPath = item.installationPath

                # msvc_info.subdir_list.append(os.path.join(msvc_info.installationPath, r'Common7\Tools\vsdevcmd\ext'))
                msvc_info.subdir_list.append(os.path.join(msvc_info.installationPath, r'VC\Auxiliary\Build'))

                msvc_info_list.append(msvc_info)

                # textfmt = self._logfmt.blue('productPath')
                # logger.info(textfmt + '={0}'.format(msvc_info.productPath))

                # textfmt = self._logfmt.blue('displayName')
                # logger.info(textfmt + '={0}'.format(msvc_info.displayName))

                # textfmt = self._logfmt.blue('buildVersion')
                # logger.info(textfmt + '={0}'.format(msvc_info.buildVersion))

                # textfmt = self._logfmt.blue('productLineVersion')
                # logger.info(textfmt + '={0}'.format(msvc_info.productLineVersion))

                # textfmt = self._logfmt.blue('installationPath')
                # logger.info(textfmt + '={0}'.format(msvc_info.installationPath))

        return msvc_info_list

    def _find_vcvars(self, msvc_info_list: list):
        found_count: int = 0

        pattern = r'vcvars[\S|_]+\d+'

        path = osdp_path()

        for item in msvc_info_list:
            item: msvc_information = item
            item.vcvars_files.clear()

            for subdir in item.subdir_list:
                if path.exist(subdir):
                    file_list1 = path.explore_dir_re(subdir, ['.bat'], pattern)
                    item.vcvars_files.extend(file_list1)
                    found_count += len(item.vcvars_files)

            # for vcvar_file in item.vcvars_files:
            #     file_field = self._logfmt.blue('File')
            #     logger.info(file_field + '={0}'.format(vcvar_file))

        return msvc_info_list

    def _dump_vcvars(self, vcvarsbat_loc):
        dirname = os.path.dirname(vcvarsbat_loc)
        basename = os.path.basename(vcvarsbat_loc)
        command = basename + "&&set"
        retrs: result = self._exec.exec(command, [], workdir=dirname)
        jsondata = {}
        if 0 == retrs.errcode:
            data = "\n".join(retrs.stdout)
            regex = re.compile(r'^(.*?)=(.*)$', re.MULTILINE)
            m = regex.findall(data)
            for item in m:
                jsondata[item[0]] = item[1]

        return jsondata
