# -*- coding: utf-8 -*-
import os
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

    bld_system: build_system
    bld_compiler: build_compiler
    project_dir: str
    build_dir: str

    def __init__(self,
                 bld_system: build_system,
                 bld_compiler: build_compiler,
                 project_dir: str,
                 build_dir: str):

        self.envdata = {}
        self.proc = process()
        self.oskind = os_helper().get_oskind()

        self.bld_system = bld_system
        self.bld_compiler = bld_compiler
        self.project_dir = project_dir
        self.build_dir = build_dir

        if ((bld_compiler.value >= build_compiler.clang.value) and
           (bld_compiler.value < build_compiler.clang_last.value)):
            self.envdata = os.environ
            self.envdata['CC'] = 'clang'
            self.envdata['CXX'] = 'clang++'

        elif ((bld_compiler.value >= build_compiler.gcc.value) and
              (bld_compiler.value < build_compiler.gcc_last.value)):
            self.envdata = os.environ
            self.envdata['CC'] = 'gcc'
            self.envdata['CXX'] = 'g++'

        elif ((bld_compiler.value >= build_compiler.msvc.value) and
              (bld_compiler.value < build_compiler.msvc_last.value)):
            self.envdata = self._get_msbuild_envdata()
            self.envdata['CC'] = 'cl'
            self.envdata['CXX'] = 'cl'

    def _get_msbuild_envdata(self,
                             msvc_ver: msvc_version = None,
                             msvc_edi: msvc_edition = None):
        if not os_helper().is_windows(self.oskind):
            return

        self.msbld = msbuild()
        supported_msvc_list = self.msbld.get_supported()
        if 0 == len(supported_msvc_list):
            return None

        if msvc_ver is None and msvc_edi is None:
            msvc_info: msvc_information = supported_msvc_list[0]
            msvc_ver = msvc_info.version
            msvc_edi = msvc_info.edition

        envdata = self.msbld.dump_vcvars(msvc_info.edition,
                                         msvc_info.version)
        return envdata

    def probe(self) -> result:
        compiler = self.envdata['CC']
        argument = []
        if ((self.bld_compiler.value >= build_compiler.msvc.value) and
           (self.bld_compiler.value < build_compiler.msvc_last.value)):
            argument = []
        else:
            argument = ['--version']

        retrs: result = self.proc.exec(compiler,
                                       argument,
                                       env=self.envdata)
        return retrs

    def config(self) -> result:
        retrs: result = self.probe()
        if 0 != retrs.errcode:
            return retrs

        retrs: result = self.proc.exec('cmake',
                                       ['-G', 'Ninja',
                                        '-B', self.build_dir],
                                       workdir=self.project_dir,
                                       env=self.envdata)
        return retrs

    def build(self) -> result:
        retrs: result = self.probe()
        if 0 != retrs.errcode:
            return retrs

        retrs: result = self.proc.exec('cmake',
                                       ['--build', self.build_dir],
                                       workdir=self.project_dir,
                                       env=self.envdata)
        return retrs
