__author__ = 'levixie@gmail.com'
import cPickle
import logging
import logging.handlers
import SocketServer
import struct
import sys
import traceback

import os
from common import slogger

logger = logging.getLogger(__name__)

_logdir = None

def set_log_dir(log_dir):
    global _logdir
    _logdir = log_dir

def un_pickle(data):
    return cPickle.loads(data)

class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while 1:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = un_pickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handle_log_record(record)

    def handle_log_record(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.__dict__.get('log_name') or record.name
        cur_logger = slogger.get_logger(_logdir, name, logging.DEBUG)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        cur_logger.handle(record)


class LogRecordSocketReceiverBase(SocketServer.TCPServer):
    """simple TCP socket-based logging receiver suitable for testing.
    """
    abort = False
    logname = None

    def serve_until_stopped(self):
        import select

        abort = False

        while not abort:
            try:
                rd, wr, ex = select.select([self.socket.fileno()],
                                           [], [],
                                           self.timeout)
                if rd:
                    self.handle_request()

            except:
                err = sys.exc_info()[0]
                logger.error('error {}\n{}'.format(err, traceback.format_exc()))
                self.abort = True
            abort = self.abort


class LogRecordTCPSocketReceiver(SocketServer.ThreadingTCPServer,
                                 LogRecordSocketReceiverBase):
    """simple TCP socket-based logging receiver suitable for testing.
    """

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler, False)
        self.allow_reuse_address = True
        self.timeout = 1
        self.abort = False
        self.server_bind()
        self.server_activate()


class LogRecordUnixSocketReceiver(SocketServer.ThreadingUnixStreamServer,
                                  LogRecordSocketReceiverBase):

    """simple Unix socket-based logging receiver suitable for testing.
    """

    def __init__(self,
                 host=None,
                 handler=LogRecordStreamHandler):
        if os.path.exists(host):
            logger.warning('%s is using', host)
            os.unlink(host)

        self.host = host
        SocketServer.ThreadingUnixStreamServer.__init__(self, host, handler)

    def server_close(self):
        os.unlink(self.host)
