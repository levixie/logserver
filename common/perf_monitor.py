__author__ = 'jesse'

from contextlib import contextmanager
import time
from datetime import datetime
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from thrift_gen.log_record import LogCollector
from thrift_gen.log_record.ttypes import PerfRecord, CounterType

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
    def get_perf(self, perf_name=None, log_dur=True):
        counter = PerfCounter()
        start_time = datetime.utcnow()
        try:
            yield counter
        finally:
            if self.client is None and self.host:
                self.create_client()

            if counter.start_time is None:
                counter.dur_sec.append((datetime.utcnow() - start_time).total_seconds())
            if not log_dur:
                counter.dur_sec = []

            recs = []
            if counter.total:
                recs.append(PerfRecord(perf_name, CounterType.TOTAL, times=counter.total, period=counter.dur_sec))
            if counter.error:
                recs.append(PerfRecord(perf_name, CounterType.ERR, times=counter.error))

            if self.client is None:
                return

            try:
                self.client.perf(recs)
            except (OSError, TTransport.TTransportException) as err:
                print err
                self.client = None  # so we can call createSocket next time
                self.transport.close()
            except Exception as err:
                print err
                self.client = None  # so we can call createSocket next time
                self.transport.close()


class PerfCounter(object):
    def __init__(self):
        self._total = 0
        self._error = 0
        self.start_time = None
        self._dur_sec = []

    def count_total(self):
        self._total += 1

    def start_period(self):
        self.start_time = datetime.utcnow()

    def end_period(self):
        dur_sec = (datetime.utcnow() - self.start_time).total_seconds()
        self._dur_sec.append(dur_sec)
        self.start_time = datetime.utcnow()

    @property
    def dur_sec(self):
        return self._dur_sec

    @dur_sec.setter
    def dur_sec(self, value):
        self._dur_sec = value

    @property
    def total(self):
        return self._total

    def count_error(self):
        self._error += 1

    @property
    def error(self):
        return self._error


def get_perf_count(name, log_dur=True):
    def wrapper(func):
        def call(*args, **kwargs):
            if _Per_Monitor is None:
                return func(*args, **kwargs)
            with _Per_Monitor.get_perf(name, log_dur=log_dur) as counter:
                try:
                    counter.start_period()
                    counter.count_total()
                    return func(*args, **kwargs)
                except:
                    counter.count_error()
                    raise
                finally:
                    counter.end_period()
        return call
    return wrapper

def get_perf_count_without_dur(name):
    return get_perf_count(name, log_dur=False)
