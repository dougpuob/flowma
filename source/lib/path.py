# -*- coding: utf-8 -*-
import os
import re

from .log import logger
from .define import os_kind
from .define import os_helper


class osdp_path():

    def __init__(self):
        pass

    def remove_dot_path(self, path: str, is_root: bool, os_sep: str):
        path_list = path.split(os_sep)
        idx = 0
        while idx < len(path_list):
            if path_list[idx] == '.':
                path_list.pop(idx)
                idx = idx - 1
            elif path_list[idx] == '..':
                if idx > 0:
                    path_list.pop(idx)
                    if is_root and idx == 1:
                        continue
                    path_list.pop(idx-1)
                    idx = idx - 2
                else:
                    path_list.pop(idx)
            idx = idx + 1
        return os_sep.join(path_list)

    def basename(self, path: str):
        fslash = path.rfind('/')
        bslash = path.rfind('\\')
        pos = max(fslash, bslash)
        if pos >= 0:
            return path[pos+1:]
        else:
            return path

    def normpath(self, path: str, os_kind: os_kind = None):
        if os_kind is not None:
            if os_kind == os_helper().is_windows(os_kind):
                return self.normpath_windows(path)
            else:
                return self.normpath_posix(path)

        is_root_win = (path.find(':') >= 0)
        is_root_unix = path.startswith('/')

        os_sep = ''
        new_path = ''
        if is_root_win:
            new_path = path.replace('/', '\\')
            os_sep = '\\'
        elif is_root_unix:
            new_path = path.replace('\\', '/')
            os_sep = '/'
        else:
            fslash_c = 0
            bslash_c = 0
            arr = list(path)
            for c in arr:
                if c == '/':
                    fslash_c = fslash_c + 1
                elif c == '\\':
                    bslash_c = bslash_c + 1
                else:
                    pass
            if fslash_c >= bslash_c:
                os_sep = '/'
                new_path = path.replace('\\', os_sep)

            else:
                os_sep = '\\'
                new_path = path.replace('/', os_sep)

        is_root = is_root_win or is_root_unix
        new_path = self.remove_dot_path(new_path, is_root, os_sep)
        return new_path

    def is_abs(self, path: str):
        is_root_win = (path.find(':') != -1)
        is_root_unix = path.startswith('/')
        return is_root_win or is_root_unix

    def is_rel(self, path: str):
        return not self.is_abs(path)

    def normpath_posix(self, path: str) -> str:
        new_path = path.replace('\\', '/')
        is_root = (new_path.find('/') != -1)
        new_path = self.remove_dot_path(new_path, is_root, '\\')
        return new_path

    def normpath_windows(self, path: str) -> str:
        new_path = path.replace('/', '\\')
        is_root = (new_path.find(':') != -1)
        new_path = self.remove_dot_path(new_path, is_root, '\\')
        return new_path

    def realpath(self, path: str) -> str:
        new_path = os.path.realpath(path)
        new_path = self.normpath(new_path)
        return new_path

    def realpath_windows(self, path: str) -> str:
        new_path = os.path.realpath(path)
        return self.normpath_windows(new_path)

    def realpath_posix(self, path: str) -> str:
        new_path = os.path.realpath(path)
        return self.normpath_posix(new_path)

    def relpath(self, path1: str, path2: str) -> str:
        path1 = self.realpath(path1)
        path2 = self.realpath(path2)
        short = ''
        long = ''
        ret = ''
        if len(path1) > len(path2):
            short = path2
            long = path1
            ret = long.replace(short, '')
        elif len(path1) < len(path2):
            short = path1
            long = path2
            ret = long.replace(short, '')
        else:
            pass

        return ret

    def exist(self, path: str):
        return os.path.exists(path)

    def explore_dir(self,
                    root_path,
                    ext_name_list: list = [],
                    prefix: str = None,
                    recurs: bool = False) -> list:

        found_list: list = []
        root_path = os.path.abspath(root_path)
        for dirname, subdir_list, file_list in os.walk(root_path,
                                                       topdown=False):
            for file in file_list:
                is_start_matched = True
                is_end_matched = True

                if prefix:
                    is_start_matched = file.startswith(prefix)

                for ext_name in ext_name_list:
                    is_end_matched = file.endswith(ext_name)
                    if is_end_matched:
                        break

                if is_start_matched and is_end_matched:
                    abspath = os.path.join(root_path, dirname, file)
                    normpath = os.path.normpath(abspath)
                    found_list.append(normpath)

        return found_list

    def explore_dir_re(self,
                       root_path,
                       ext_name_list: list = [],
                       regex_pattern: str = None,
                       recurs: bool = False) -> list:

        found_list: list = []
        root_path = os.path.abspath(root_path)
        for dirname, subdir_list, file_list in os.walk(root_path,
                                                       topdown=False):
            for file in file_list:
                is_start_matched = True
                is_end_matched = True

                for ext_name in ext_name_list:
                    is_end_matched = file.endswith(ext_name)
                    if is_end_matched:
                        break

                if regex_pattern and is_end_matched:
                    filename = os.path.basename(file)
                    result = re.match(regex_pattern, filename)
                    is_start_matched = (result is not None)

                if is_start_matched and is_end_matched:
                    abspath = os.path.join(root_path, dirname, file)
                    normpath = os.path.normpath(abspath)
                    found_list.append(normpath)

        return found_list
