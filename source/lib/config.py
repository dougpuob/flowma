# -*- coding: utf-8 -*-
from asyncio import windows_events
import os
import platform

from enum import Enum


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


class os_helper():

    def __init__(self):
        pass

    def is_windows(self, osk: os_kind):
        return osk.value >= os_kind.windows.value or \
               osk.value < os_kind.windows_max.value

    def is_linux(self, osk: os_kind):
        return osk.value >= os_kind.linux.value or \
               osk.value < os_kind.linux_max.value

    def is_macos(self, osk: os_kind):
        return osk.value >= os_kind.macos.value or \
               osk.value < os_kind.macos_max.value
