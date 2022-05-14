# -*- coding: utf-8 -*-

from enum import Enum


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
    x86_32 =  x86_default + 1
    x86_64 =  x86_default + 2

    arm = 2000

    riscv = 3000