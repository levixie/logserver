__author__ = 'jesse'

from threading import Thread, Timer, RLock
from collections import defaultdict
import logging
import time
from datetime import datetime
import heapq

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
        self.total_req_times = defaultdict(lambda: {'t': 0, 'p': 0.0})
        self.req_times_heaps = defaultdict(lambda: [])

    def run(self):
        self.log.info("START of PerfCollector::run")
        while True:
            recs = self.perf_rec_queue.get()
            for rec in recs:
                with _lock:
                    if rec.period:
                        for period in rec.period:
                            self.total_req_times[rec.id]['t'] += 1
                            self.total_req_times[rec.id]['p'] += period
                            heapq.heappush(self.req_times_heaps[rec.id], period)
                    if rec.type == CounterType.ERR:
                        self.err_counters[rec.id] += rec.times
                    elif rec.type == CounterType.TOTAL:
                        self.counters[rec.id] += rec.times

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
                    self.send_counter("{}".format(name), counter)
                    if counter == 0:
                        self.collector.counters.pop(name)
                    else:
                        self.collector.counters[name] = 0

                for name, counter in self.collector.err_counters.items():
                    self.send_counter("{}_err".format(name), counter)
                    if counter == 0:
                        self.collector.err_counters.pop(name)
                    else:
                        self.collector.err_counters[name] = 0

                for name, dur in self.collector.total_req_times.items():
                    self.send_period("{}_avg".format(name), dur['t'], dur['p'])
                    self.collector.total_req_times.pop(name)
                    ninetieth_element = self.collector.req_times_heaps[name][int(dur['t']*0.9)]
                    self.send_period("{}_90th".format(name), 1, ninetieth_element)
                    self.collector.req_times_heaps.pop(name)

    def send_counter(self, name, counter):
        self.log.info("{}_hits is {}".format(name, counter/self.interval))

    def send_period(self, name, times, dur_period):
        self.log.info("{}_dur is {}".format(name, dur_period/times))
