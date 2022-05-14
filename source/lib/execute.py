# -*- coding: utf-8 -*-
import os
import logging
import subprocess


class result():
    def __init__(self):
        self.errcode = 0
        self.stdout = []
        self.stderr = []
        self.data = b''


class process():

    ret: result = result()
    proc = None

    def __init__(self) -> None:
        pass

    def run(self, program: str,
            arguments: list = [],
            workdir: str = os.getcwd(),
            timeout: int = None) -> result:
        try:
            cmdargs = [program]
            cmdargs.extend(arguments)
            logging.info('cmdargs={}'.format(cmdargs))

            self.proc = subprocess.Popen(cmdargs,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         shell=False,
                                         cwd=workdir)
            try:
                outs, errs = self.proc.communicate(timeout)

                stdout = outs.decode('utf-8', errors="ignore")
                stdout = stdout.replace('\r', '')
                stdout_lines = stdout.split('\n')
                self.ret.stdout.extend(stdout_lines)

                stderr = errs.decode('utf-8', errors="ignore")
                stdout = stderr.replace('\r', '')
                stderr_lines = stderr.split('\n')
                self.ret.stderr.extend(stderr_lines)

                self.ret.errcode = self.proc.returncode

            except subprocess.TimeoutExpired as Err:
                logging.exception(Err)
                self.ret.errcode = 100000
                self.ret.stderr.append(Err)
                self.proc.kill()

            except Exception as Err:
                logging.exception(Err)
                self.ret.errcode = 100000
                self.ret.stderr.append(Err)
                self.proc.kill()

        except subprocess.TimeoutExpired as Err:
            logging.exception(Err)
            self.ret.errcode = 100001
            self.ret.stderr.append(Err)

        except Exception as Err:
            logging.exception(Err)
            self.ret.errcode = 100002
            self.ret.stderr.append(Err)

        finally:
            return self.ret
