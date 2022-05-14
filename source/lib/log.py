# -*- coding: utf-8 -*-
import logging


class logger_format(logging.Formatter):

    _BLUE_: str = "\x1b[38;5;39m"
    _GREY_: str = "\x1b[38;20m"
    _YELLOW_: str = "\x1b[33;20m"
    _RED_: str = "\x1b[31;20m"
    _RED_BOLD_: str = "\x1b[31;1m"
    _RESET_: str = "\x1b[0m"
    _FORMAT_: str = '[%(asctime)s][%(levelname)-8s] %(message)s'

    FORMATS = {
        logging.DEBUG: _GREY_ + _FORMAT_ + _RESET_,
        logging.INFO: _GREY_ + _FORMAT_ + _RESET_,
        logging.WARNING: _YELLOW_ + _FORMAT_ + _RESET_,
        logging.ERROR: _RED_ + _FORMAT_ + _RESET_,
        logging.CRITICAL: _RED_BOLD_ + _FORMAT_ + _RESET_
    }

    def blue(self, text: str) -> str:
        newtext: str = self._BLUE_ + text + self._RESET_
        return newtext

    def red(self, text: str) -> str:
        newtext: str = self._RED_ + text + self._RESET_
        return newtext

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

    def get_logger(self, name: str = 'flowma'):
        cmzfmt = logger_format()
        screen = logging.StreamHandler()
        screen.setFormatter(cmzfmt)
        logger = logging.getLogger()
        logger.addHandler(screen)
        logger.setLevel(logging.INFO)

        return logger


logger = logger_format().get_logger()
