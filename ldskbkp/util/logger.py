import logging
import sys
import os

from ldskbkp.util.misc import does_terminal_support_color

_log_format_file = "%(asctime)s - [%(levelname)-7s] - ldbk: %(filename)16s:%(lineno)-3s | %(message)s"

_colourful_terminal = does_terminal_support_color()

_log_format_stdout_info = "%(message)s"
_log_format_stdout_warning = "WARNING: %(message)s"
_log_format_stdout_error = "ERROR: %(message)s"

loggers = {}

default_level = logging.INFO


class LDBKStdOutFormatter(logging.Formatter):

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS_COLORED = {
        logging.DEBUG: grey + _log_format_stdout_info + reset,
        logging.INFO: grey + _log_format_stdout_info + reset,
        logging.WARNING: yellow + _log_format_stdout_warning + reset,
        logging.ERROR: red + _log_format_stdout_error + reset,
        logging.CRITICAL: bold_red + _log_format_stdout_error + reset
    }

    FORMATS_NON_COLORED = {
        logging.DEBUG: _log_format_stdout_info,
        logging.INFO: _log_format_stdout_info,
        logging.WARNING: _log_format_stdout_warning,
        logging.ERROR: _log_format_stdout_error,
        logging.CRITICAL: _log_format_stdout_error
    }

    def format(self, record):
        if _colourful_terminal:
            log_fmt = self.FORMATS_COLORED.get(record.levelno)
        else:
            log_fmt = self.FORMATS_NON_COLORED.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_stream_handlers(logpath, logfile=False, level=logging.INFO, ):
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(LDBKStdOutFormatter())

    if logfile:
        stream_handler_file = logging.FileHandler(logpath, encoding='utf-8')
        stream_handler_file.setLevel(level)
        stream_handler_file.setFormatter(logging.Formatter(_log_format_file))
        return stream_handler, stream_handler_file
    else:
        return stream_handler,


def get_logger(name="ldbk", level=None, logfile=False, logpath=os.getcwd()):
    global default_level
    if level is None:
        level = default_level
    if name in loggers:
        if loggers[name].level == level:
            return loggers[name]
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []
    for ahandler in get_stream_handlers(logpath, level=level, logfile=logfile):
        logger.addHandler(ahandler)
    loggers[name] = logger
    return loggers[name]


def setdebug():
    global default_level
    default_level = logging.DEBUG


def getdebug():
    return default_level == logging.DEBUG


