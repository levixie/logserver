__author__ = 'levixie@gmail.com'

import logging
import logging.handlers

import os
from log_handlers import SimpleSocketHandler, SimpleThriftHandler


def mlevel(level):
    if 'info' == level.lower():
        return logging.INFO
    elif 'debug' == level.lower():
        return logging.DEBUG
    elif 'fatal' == level.lower():
        return logging.FATAL
    return logging.INFO


def setUpLogger(log_dir, logger_name, level=None, capacity=102400, host=None, port=None, use_thrift=True):
    logger = logging.getLogger()

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if host:
        hdlr = SimpleThriftHandler(host, port, logger_name) \
            if use_thrift else SimpleSocketHandler(host, port, logger_name)
    else:
        hdlr = logging.handlers.TimedRotatingFileHandler(os.path.join(
            log_dir, '%s.log' % logger_name), when='midnight', backupCount=7)
    formatter = logging.Formatter(
        '%(asctime)s %(process)d %(name)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    log_level = logging.INFO
    if isinstance(level, (str, unicode)):
        log_level = mlevel(level)
    mhdlr = logging.handlers.MemoryHandler(capacity, log_level, hdlr)
    logger.addHandler(mhdlr)
    logger.setLevel(log_level)
    return logger

_all_local_logger = {}

def get_logger(log_dir, logger_name, level=None, capacity=102400, reset=False):
    global _all_local_logger

    if (not reset) and logger_name in _all_local_logger:
        return logging.getLogger(logger_name)

    if not log_dir:
        return None

    logger = logging.getLogger(logger_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    hdlr = logging.handlers.TimedRotatingFileHandler(os.path.join(
        log_dir, '%s.log' % logger_name), when='midnight', backupCount=7)
    formatter = logging.Formatter(
        '%(asctime)s %(process)d %(name)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    log_level = logging.INFO
    if isinstance(level, (str, unicode)):
        log_level = mlevel(level)
    mhdlr = logging.handlers.MemoryHandler(capacity, log_level, hdlr)
    logger.addHandler(mhdlr)
    logger.setLevel(log_level)

    _all_local_logger[logger_name] = True
    return logger
