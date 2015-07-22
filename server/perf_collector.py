__author__ = 'jesse'

from threading import Thread, Timer, RLock
from collections import defaultdict
import logging
import time
from datetime import datetime

from common.thrift_gen.log_record.ttypes import CounterType

logger = logging.getLogger(__name__)
_lock = RLock()

class PerfCollector(Thread):
    def __init__(self, perf_rec_queue, log):
        super(PerfCollector, self).__init__()
        self.perf_rec_queue = perf_rec_queue
        self.log = log or logger
        self.counters = defaultdict(lambda: 0)
        self.err_counters = defaultdict(lambda: 0)

    def run(self):
        self.log.info("START of PerfCollector::run")
        while True:
            recs = self.perf_rec_queue.get()
            for rec in recs:
                with _lock:
                    if rec.type == CounterType.ERR:
                        self.err_counters[rec.id] += 1
                    else:
                        self.counters[rec.id] += 1

class PerfSender(Thread):
    def __init__(self, collector, log, interval=60.0):
        super(PerfSender, self).__init__()
        self.log = log or logger
        self.collector = collector
        self.interval = interval

    def run(self):
        self.log.info("START of PerfSender::run")
        last_time = datetime.utcnow()
        while True:
            cur_time = datetime.utcnow()
            diff_sec = (cur_time - last_time).total_seconds()
            if diff_sec < self.interval:
                time.sleep(self.interval - diff_sec)
            last_time = datetime.utcnow()
            with _lock:
                for name, counter in self.collector.counters.items():
                    self.send(name, counter)
                    if counter == 0:
                        self.collector.counters.pop(name)
                    else:
                        self.collector.counters[name] = 0
                for name, counter in self.collector.err_counters.items():
                    self.send("{}_err".format(name), counter)
                    if counter == 0:
                        self.collector.err_counters.pop(name)
                    else:
                        self.collector.err_counters[name] = 0

    def send(self, name, counter):
        self.log.info("{} is {}".format(name, counter/self.interval))
