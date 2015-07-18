__author__ = 'jesse'

import logging
import logging.handlers

from common import slogger


class LogCollectorHandler(object):
    def __init__(self, log_name=None, log_dir=None):
        self.log_name = log_name
        self.log_dir = log_dir

    def log(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.log_name is not None:
            name = self.log_name
        else:
            name = record.log_name or record.name
        cur_logger = slogger.get_logger(self.log_dir, name, logging.DEBUG)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        py_record = logging.makeLogRecord(
            {'name': record.name,
             'levelno': record.level,
             'levelname': logging.getLevelName(record.level),
             'pathname': record.pathname,
             'lineno': record.lineno,
             'msg': record.msg,
             'args': None,
             'exc_info': None,
             'funcName': record.func,
             'thread': record.thread,
             'threadName': record.threadname,
             'processName': record.processname,
             'process': record.process}
        )
        cur_logger.handle(py_record)