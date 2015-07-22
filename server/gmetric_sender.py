__author__ = 'jesse'

from common.gmetric import get_gmetrics
from perf_collector import PerfSender


class GMetricSender(PerfSender):
    def __init__(self, collector, log, interval=60.0, cfg_path='/etc/ganglia/gmond.conf'):
        super(GMetricSender, self).__init__(collector, log, interval)
        self.metrics = get_gmetrics(cfg_path)

    def send(self, name, counter):
        value = counter/self.interval
        group_name = ''
        if name.find('|') != -1:
            group_name, name = name.rsplit('|', 2)
        count_name = "{}_hits".format(name)
        self.log.info("group:{} name:{} value:{}".format(group_name, count_name, value))

        for metric in self.metrics:
            metric.send(count_name, value,
                        TYPE='float', UNITS='count',
                        GROUP=group_name, DMAX=3600)
