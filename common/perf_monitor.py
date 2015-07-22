__author__ = 'jesse'

from contextlib import contextmanager
import time
from collections import defaultdict
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from thrift_gen.log_record import LogCollector
from thrift_gen.log_record.ttypes import LogRecord, CounterRecord, CounterType

_Per_Monitor = None

class PerfMonitor(object):
    @staticmethod
    def set_instance(host=None, port=None):
        global _Per_Monitor
        _Per_Monitor = PerfMonitor(host, port)
        return _Per_Monitor

    @staticmethod
    def get_instance():
        if _Per_Monitor is None:
            PerfMonitor.set_instance()
        return _Per_Monitor

    def __init__(self, host, port=None):
        self.host = host
        self.port = port
        self.client = None
        self.retryTime = None
        self.transport = None
        self.retryPeriod = None
        #
        # Exponential backoff parameters.
        #
        self.retryStart = 1.0
        self.retryMax = 30.0
        self.retryFactor = 2.0

    def create_client(self):
        now = time.time()
        if self.retryTime is None:
            attempt = True
        else:
            attempt = (now >= self.retryTime)
        if attempt:
            try:
                socket = TSocket.TSocket(self.host, self.port) if self.port else TSocket.TSocket(unix_socket=self.host)
                self.transport = TTransport.TFramedTransport(socket)
                protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
                self.client = LogCollector.Client(protocol)
                self.transport.open()
                self.retryTime = None  # next time, no delay before trying
            except TTransport.TTransportException as err:
                print err
                # Creation failed, so set the retry time and return.
                if self.retryTime is None:
                    self.retryPeriod = self.retryStart
                else:
                    self.retryPeriod *= self.retryFactor
                    if self.retryPeriod > self.retryMax:
                        self.retryPeriod = self.retryMax
                self.retryTime = now + self.retryPeriod

    @contextmanager
    def get_counter(self, counter_name=None):
        counter = PerfCounter()
        try:
            yield counter
        finally:
            if self.client is None and self.host:
                self.create_client()

            recs = []
            if counter.total:
                recs.append(CounterRecord(counter_name, CounterType.TOTAL))
            if counter.error:
                recs.append(CounterRecord(counter_name, CounterType.ERR))

            if self.client is None:
                return

            try:
                self.client.count(recs)
            except (OSError, TTransport.TTransportException) as err:
                print err
                self.client = None  # so we can call createSocket next time
                self.transport.close()
            except Exception as err:
                print err
                if not hasattr(err, 'errno') or (err.errno != 32 and err.errno != 57):
                    raise
                self.client = None  # so we can call createSocket next time
                self.transport.close()


class PerfCounter(object):
    def __init__(self):
        self._total = 0
        self._error = 0

    def count_total(self):
        self._total += 1

    @property
    def total(self):
        return self._total

    def count_error(self):
        self._error += 1

    @property
    def error(self):
        return self._error


def get_perf_count(name):
    def wrapper(func):
        def call(*args, **kwargs):
            if _Per_Monitor is None:
                return func(*args, **kwargs)
            with _Per_Monitor.get_counter(name) as counter:
                try:
                    counter.count_total()
                    return func(*args, **kwargs)
                except:
                    counter.count_error()
                    raise
        return call
    return wrapper
