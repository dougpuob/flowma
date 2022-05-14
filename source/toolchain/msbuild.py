# -*- coding: utf-8 -*-
import os

from enum import Enum
from define import msvc_edition, msvc_version


class msvc_information():
    version: msvc_version
    edition: msvc_edition
    rootdir: str
    vcvars_files: list

    def __init__(self, ver, edi, rootdir) -> None:
        self.version = ver,
        self.edition = edi
        self.rootdir = rootdir


class vcvars():
    default_msvc_list = []

    def __init__(self) -> None:

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
        self.default_msvc_list.append(msvc_information(msvc_version.vs2022, msvc_edition.enterprise,   r'C:\Program Files\Microsoft Visual Studio\2022\BuildTools'))
        self.default_msvc_list.append(msvc_information(msvc_version.vs2022, msvc_edition.community,    r'C:\Program Files\Microsoft Visual Studio\2022\Community'))
        self.default_msvc_list.append(msvc_information(msvc_version.vs2022, msvc_edition.professional, r'C:\Program Files\Microsoft Visual Studio\2022\Professional'))
        self.default_msvc_list.append(msvc_information(msvc_version.vs2022, msvc_edition.enterprise,   r'C:\Program Files\Microsoft Visual Studio\2022\Community'))


        # vs2019
        self.default_msvc_list.append(msvc_information(msvc_version.vs2019, msvc_edition.enterprise,   r'C:\Program Files\Microsoft Visual Studio\2019\BuildTools'))
        self.default_msvc_list.append(msvc_information(msvc_version.vs2019, msvc_edition.community,    r'C:\Program Files\Microsoft Visual Studio\2019\Community'))
        self.default_msvc_list.append(msvc_information(msvc_version.vs2019, msvc_edition.professional, r'C:\Program Files\Microsoft Visual Studio\2019\Professional'))
        self.default_msvc_list.append(msvc_information(msvc_version.vs2019, msvc_edition.enterprise,   r'C:\Program Files\Microsoft Visual Studio\2019\Community'))

        # vs2017
        self.default_msvc_list.append(msvc_information(msvc_version.vs2017, msvc_edition.community,    r'C:\Program Files\Microsoft Visual Studio\2017\Community'))
        self.default_msvc_list.append(msvc_information(msvc_version.vs2017, msvc_edition.professional, r'C:\Program Files\Microsoft Visual Studio\2017\Professional'))
        self.default_msvc_list.append(msvc_information(msvc_version.vs2017, msvc_edition.enterprise,   r'C:\Program Files\Microsoft Visual Studio\2017\Community'))


    def find_vcvars_files(self,
                          msvc_ver: msvc_version = msvc_version.vs2019,
                          msvc_edi: msvc_edition = msvc_edition.community,
                          dirpath: str = None) -> str:

        subdir1 = 'Common7\Tools\vsdevcmd\ext'
        subdir2 = 'VC\Auxiliary\Build'

        for item in self.default_msvc_list:
            item: msvc_information = item
            path1 = os.path.join(item.rootdir, subdir1)
            path2 = os.path.join(item.rootdir, subdir2)