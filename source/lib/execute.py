# -*- coding: utf-8 -*-
import os
import locale
import logging
import subprocess


class result():
    def __init__(self):
        self.errcode = 0
        self.stdout = []
        self.stderr = []
        self.data = b''


class process():

    proc = None

    def __init__(self) -> None:
        pass

    def run(self, program: str,
            arguments: list = [],
            workdir: str = os.getcwd(),
            timeout: int = None) -> result:
        try:
            ret: result = result()
            cmdargs = [program]
            cmdargs.extend(arguments)
            logging.info('cmdargs={}'.format(cmdargs))

            self.proc = subprocess.Popen(cmdargs,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         shell=True,
                                         cwd=workdir)
            try:
                loc = locale.getlocale()
                outs, errs = self.proc.communicate(timeout)

                stdout = outs.decode(loc[-1])
                stdout = stdout.replace('\r', '')
                stdout_lines = stdout.split('\n')
                ret.stdout.extend(stdout_lines)

                stderr = errs.decode(loc[-1])
                stdout = stderr.replace('\r', '')
                stderr_lines = stderr.split('\n')
                ret.stderr.extend(stderr_lines)

                ret.errcode = self.proc.returncode

            except subprocess.TimeoutExpired as Err:
                logging.exception(Err)
                ret.errcode = 100000
                ret.stderr.append(Err)
                self.proc.kill()

            except Exception as Err:
                logging.exception(Err)
                ret.errcode = 100000
                ret.stderr.append(Err)
                self.proc.kill()

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
