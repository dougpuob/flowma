# -*- coding: utf-8 -*-
import json

from ..lib.execute import process, result
from ..lib.define import build_system, build_compiler, os_helper, os_kind
from ..lib.define import msvc_edition, msvc_version

from ..toolchain.msbuild import msbuild, msvc_information


class flowma_build():
    oskind: os_kind
    proc: process
    msbld: msbuild

    envdata: json

    project_dir: str
    build_dir: str

    def __init__(self,
                 system: build_system,
                 compiler: build_compiler,
                 project_dir: str,
                 build_dir: str):
        self.proc = process()
        self.oskind = os_helper().get_oskind()

        self.project_dir = project_dir
        self.build_dir = build_dir

        if system.msbuild.value == build_system.msbuild.value:
            self.envdata = self._get_msbuild_envdata()

    def _get_msbuild_envdata(self,
                             msvc_ver: msvc_version = None,
                             msvc_edi: msvc_edition = None):
        if not os_helper().is_windows(self.oskind):
            return

        self.msbld = msbuild()
        supported_msvc_list = self.msbld.get_supported()
        if 0 == len(supported_msvc_list):
            return None

        msvc_info: msvc_information = msvc_information()
        if msvc_ver is None and msvc_edi is None:
            msvc_info: msvc_information = supported_msvc_list[0]
            msvc_ver = msvc_info.version
            msvc_edi = msvc_info.edition

        envdata = self.msbld.dump_vcvars(msvc_info.edition,
                                         msvc_info.version)

        return envdata

    def config(self) -> result:
        retrs: result = self.proc.exec('cmake',
                                       ['-G', 'Ninja',
                                        '-B', self.build_dir],
                                       workdir=self.project_dir)
        return retrs

    def build(self) -> result:
        retrs: result = self.proc.exec('cmake',
                                       ['--build', self.build_dir],
                                       workdir=self.project_dir)
        return retrs
