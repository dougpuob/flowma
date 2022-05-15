# -*- coding: utf-8 -*-

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
    unknown = 0

    vs2015 = 1
    vs2017 = 2
    vs2019 = 3
    vs2022 = 4

    last = 5


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


class cpu_bits(Enum):
    _32bit = 1
    _64bit = 2


class cpu_arch(Enum):
    unknown = 0

    x86_default = 1000
    x86_32 = x86_default + 1
    x86_64 = x86_default + 2

    arm = 2000

    riscv = 3000


class config():
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

    def __init__(self):
        pass

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

    def is_windows(self, osk: os_kind):
        return osk.value >= os_kind.windows.value or \
               osk.value < os_kind.windows_max.value

    def is_linux(self, osk: os_kind):
        return osk.value >= os_kind.linux.value or \
               osk.value < os_kind.linux_max.value

    def is_macos(self, osk: os_kind):
        return osk.value >= os_kind.macos.value or \
               osk.value < os_kind.macos_max.value
