# -*- coding: utf-8 -*-
import os
import json
import locale
import logging
import subprocess


from .define import os_helper, os_kind


class result():
    def __init__(self):
        self.errcode = 0
        self.stdout = []
        self.stderr = []
        self.data = b''


class process():

    cur_osk: os_kind

    def __init__(self) -> None:
        self.cur_osk = os_helper().get_oskind()

    def shell(self,
              program: str,
              arguments: list = [],
              workdir: str = os.getcwd(),
              env: json = None,
              timeout: int = None) -> result:
        return self._exec(program, arguments, workdir, env, timeout,
                          shell=True)

    def exec(self,
             program: str,
             arguments: list = [],
             workdir: str = os.getcwd(),
             env: json = None,
             timeout: int = None) -> result:

        shell: bool = False
        if self.cur_osk.value == os_kind.windows.value:
            shell = True

        return self._exec(program, arguments, workdir, env, timeout, shell)

    def _exec(self,
              program: str,
              arguments: list = [],
              workdir: str = os.getcwd(),
              env: json = None,
              timeout: int = None,
              shell: bool = True) -> result:
        try:
            ret: result = result()
            cmdargs = [program]
            cmdargs.extend(arguments)
            logging.debug('cmdargs={}'.format(cmdargs))

            proc = subprocess.Popen(cmdargs,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=shell,
                                    cwd=workdir,
                                    env=env)
            try:
                loc_data = locale.getlocale()

                # loc_index = 0
                # for loc in loc_data:
                #     logging.info('locale[{}]={}'.format(loc_index, loc))
                #     loc_index += 1

                outs, errs = proc.communicate(timeout)

                stdout = outs.decode(loc_data[-1])
                stdout = stdout.replace('\r', '')
                stdout_lines = stdout.split('\n')
                ret.stdout.extend(stdout_lines)

                stderr = errs.decode(loc_data[-1])
                stdout = stderr.replace('\r', '')
                stderr_lines = stderr.split('\n')
                ret.stderr.extend(stderr_lines)

                ret.errcode = proc.returncode

            except subprocess.TimeoutExpired as Err:
                logging.exception(Err)
                ret.errcode = 100000
                ret.stderr.append(Err)
                proc.kill()

            except Exception as Err:
                logging.exception(Err)
                ret.errcode = 100000
                ret.stderr.append(Err)
                proc.kill()

        except subprocess.TimeoutExpired as Err:
            logging.exception(Err)
            ret.errcode = 100001
            ret.stderr.append(Err)

        except Exception as Err:
            logging.exception(Err)
            ret.errcode = 100002
            ret.stderr.append(Err)

        finally:
            return ret
