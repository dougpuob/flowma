# -*- coding: utf-8 -*-
import os
import json
import platform

from enum import Enum
from types import SimpleNamespace


class os_kind(Enum):
    unknown = 0

    windows = 1000
    windows_10 = windows + 1
    windows_11 = windows + 2
    windows_max = 1999

    linux = 2000
    linux_debian = linux + 1
    linux_ubuntu = linux + 2
    linux_max = 2999

    macos = 3000
    macos_max = 3999


class msvc_version(Enum):
    default = 0
    vs97 = 5
    vs6 = 6
    vs2002 = 7
    vs2003 = 7.1
    vs2005 = 8
    vs2008 = 9
    vs2010 = 10
    vs2012 = 11
    vs2013 = 12
    vs2015 = 14
    vs2017 = 15
    vs2019 = 16
    vs2022 = 17

    last = vs2022


class msvc_edition(Enum):
    unknown = 0

    buildtools = 1
    community = 2
    professional = 3
    enterprise = 4


class build_system(Enum):
    unknown = 0

    msbuild = 1
    xcode = 2
    makefiles = 3
    ninja = 4


class build_compiler(Enum):
    unknown = 0

    msvc = msvc_version.default.value
    msvc_2015 = msvc_version.vs2015.value
    msvc_2017 = msvc_version.vs2017.value
    msvc_2019 = msvc_version.vs2019.value
    msvc_2022 = msvc_version.vs2022.value
    msvc_last = msvc_2022 + 1

    gcc = 100
    gcc_last = gcc + 1

    clang = 200
    clang_last = clang + 1


class cpu_bits(Enum):
    _32bit = 1
    _64bit = 2


class cpu_architecture(Enum):
    unknown = 0

    x86_default = 1000
    x86_32 = x86_default + 1
    x86_64 = x86_default + 2

    arm = 2000
    arm_32 = arm + 1
    arm_64 = arm + 2

    riscv = 3000


class CONFIGURATION():
    def _try(self, o):
        try:
            return o.__dict__
        except Exception:
            return str(o).replace('\n', '')

    def toTEXT(self):
        return json.dumps(self, default=lambda o: self._try(o)).strip()

    def toJSON(self):
        return json.loads(self.toTEXT())

    def toCLASS(self, text=None):
        if not text:
            text = self.toTEXT()
        return json.loads(text, object_hook=lambda d: SimpleNamespace(**d))


class os_helper():

    cur_osk: os_kind

    def __init__(self):
        self.cur_osk = self.get_oskind()

    def get_oskind(self) -> os_kind:
        os_system = platform.system()
        if 'Windows' == os_system:
            return os_kind.windows
        elif 'Linux' == os_system:
            return os_kind.linux
        elif 'Darwin' == os_system:
            return os_kind.macos
        else:
            return os_kind.unknown

    def is_windows(self, osk: os_kind = None):
        if not osk:
            osk = self.cur_osk
        return osk.value >= os_kind.windows.value and \
            osk.value < os_kind.windows_max.value

    def is_linux(self, osk: os_kind = None):
        if not osk:
            osk = self.cur_osk
        return osk.value >= os_kind.linux.value and \
            osk.value < os_kind.linux_max.value

    def is_macos(self, osk: os_kind = None):
        if not osk:
            osk = self.cur_osk
        return osk.value >= os_kind.macos.value and \
            osk.value < os_kind.macos_max.value


class environment_variables():
    envdata: json

    def __init__(self) -> None:
        self.envdata = os.environ
        self.apply_extra_path()

    def get_default(self) -> json:
        return os.environ

    def get_applied_envdata(self) -> json:
        return self.envdata

    def apply_extra_path(self):
        extra_path: list = [r'C:\Program Files\CMake\bin']
        path_str = self.envdata['PATH']

        for extra in extra_path:
            existing = False
            path_list = path_str.split(';')
            for item in path_list:
                if item == extra:
                    existing = True
                    break
            if not existing:
                path_list.append(extra)
        self.envdata['PATH'] = ';'.join(path_list)

