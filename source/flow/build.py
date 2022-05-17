# -*- coding: utf-8 -*-
import os
import json

from ..lib.execute import process, result
from ..lib.define import build_system, build_compiler, os_helper, os_kind
from ..lib.define import msvc_edition, msvc_version

from ..toolchain.msbuild import msbuild, msvc_information


class flowma_build():

    #
    #
    #
    oskind: os_kind
    proc: process
    msbld: msbuild

    #
    #
    #
    bld_system: build_system
    bld_compiler: build_compiler
    project_dir: str
    build_dir: str

    #
    #
    #
    envdata: json
    msvc_info: msvc_information

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
            self.msbld = msbuild()
            self.msvc_info = self._match_msvc_info(bld_compiler)
            if self.msvc_info:
                self.bld_compiler = self.msvc_info.version
            self.envdata = self._get_msbuild_envdata()
            self.envdata['CC'] = 'cl'
            self.envdata['CXX'] = 'cl'

    def _match_msvc_info(self, bld_compiler: build_compiler):
        supported_msvc_list = self.msbld.get_supported()
        if 0 == len(supported_msvc_list):
            return None

        if build_compiler.msvc.value == bld_compiler.value:
            msvc_info: msvc_information = supported_msvc_list[0]
            bld_compiler = msvc_info.version

        for msvc_info in supported_msvc_list:
            msvc_info: msvc_information = msvc_info
            if msvc_info.version.value == bld_compiler.value:
                return msvc_info
        return None

    def _get_msbuild_envdata(self,
                             msvc_ver: msvc_version = None,
                             msvc_edi: msvc_edition = None):
        if not os_helper().is_windows(self.oskind):
            return {}

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

    def get_capability(self):
        capability = {}

        capability['ninja'] = 0
        capability['gcc'] = 0
        capability['clang'] = 0
        capability['clang-format'] = 0
        capability['clang-tidy'] = 0
        capability['conan'] = 0
        capability['cmake'] = 0

        capability['choco'] = 0
        capability['brew'] = 0
        capability['apt'] = 0

        capability['curl'] = 0
        capability['wget'] = 0
        capability['7zip'] = 0

        capability['msvc']['2017'] = ['buildtools',
                                      'community',
                                      'professional',
                                      'enterprise']

        capability['msvc']['2019'] = ['buildtools',
                                      'community',
                                      'professional',
                                      'enterprise']

        capability['msvc']['2022'] = ['buildtools',
                                      'community',
                                      'professional',
                                      'enterprise']

        return capability

    def _probe_cmake(self) -> result:
        binfile = 'cmake'
        argument = ['--version']
        retrs: result = self.proc.exec(binfile,
                                       argument,
                                       env=self.envdata)
        return retrs

    def _probe_cc(self) -> result:

        # Check compiler (CC)
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

    def probe(self) -> result:

        # Compiler
        retrs: result = self._probe_cc()
        if 0 != retrs.errcode:
            return retrs

        # CMake
        retrs: result = self._probe_cmake()
        if 0 != retrs.errcode:
            return retrs

        return retrs

    def config(self) -> result:
        retrs: result = self.probe()
        if 0 != retrs.errcode:
            return retrs

        if self.bld_system.value == build_system.ninja.value:
            # -DCMAKE_EXPORT_COMPILE_COMMANDS
            #  This option is implemented only by Makefile Generators and
            #  the Ninja. It is ignored on other generators.
            retrs = self.proc.exec('cmake',
                                   ['-G', 'Ninja',
                                    '-B', self.build_dir,
                                    '-DCMAKE_VERBOSE_MAKEFILE=ON',
                                    '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON'],
                                   workdir=self.project_dir,
                                   env=self.envdata)

        elif self.bld_system.value == build_system.msbuild.value:
            MsvcList = {}
            # Optional [arch] can be "Win64" or "ARM".
            MsvcList[build_compiler.msvc_2015.value] = 'Visual Studio 14 2015 [arch]'
            MsvcList[build_compiler.msvc_2017.value] = 'Visual Studio 15 2017 [arch]'
            MsvcList[build_compiler.msvc_2019.value] = 'Visual Studio 16 2019'
            MsvcList[build_compiler.msvc_2022.value] = 'Visual Studio 17 2022'

            Generator: str = MsvcList[self.bld_compiler.value]
            Generator.replace('[arch]', 'Win64')

            retrs = self.proc.exec('cmake',
                                   ['-G', Generator,
                                    '-B', self.build_dir,
                                    '-DCMAKE_VERBOSE_MAKEFILE=ON',
                                    '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON'],
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
