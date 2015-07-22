__author__ = 'levixie@gmail.com'

import logging
import logging.handlers
import argparse

import Queue
from common import slogger
from server.log_receivers import LogRecordTCPSocketReceiver, LogRecordUnixSocketReceiver, set_log_dir
from thrift_handlers import LogCollectorHandler

from perf_collector import PerfCollector, PerfSender
from gmetric_sender import GMetricSender

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser("usage: %prog [options]")

    parser.add_argument('-b', '--bind', dest='host',
                        metavar='ADDR',
                        help='IP addr or hostname to bind to')
    parser.add_argument('-p', '--port', dest='port', type=int,
                        metavar='PORT',
                        help='port to bind to')
    parser.add_argument('-d', '--logdir', dest='logdir',
                        metavar='LOGDIR', default='.',
                        help='log DIR')
    parser.add_argument('-l', '--loglevel', dest='loglevel',
                        metavar='LOGLEVEL', default='DEBUG',
                        help='log flag')
    parser.add_argument('--thrift', dest='use_thrift',
                        metavar='THRIFT', default=True,
                        help='use thrift or not')
    parser.add_argument('--gcfg', dest='gcfg',
                        metavar='GMONDCFG', default='/usr/local/etc/gmond.cfg',
                        help='gmond location')

    args = parser.parse_args()

    global logger
    logger = slogger.get_logger(args.logdir, 'logserver', args.loglevel)

    if args.use_thrift:
        from common.thrift_gen.log_record import LogCollector
        from thrift.transport import TSocket
        from thrift.protocol import TBinaryProtocol
        from thrift.server import TNonblockingServer

        perf_rec_queue = Queue.Queue()
        handler = LogCollectorHandler(perf_rec_queue=perf_rec_queue)

        processor = LogCollector.Processor(handler)
        transport = TSocket.TServerSocket(host=args.host, port=args.port) \
            if args.port else TSocket.TServerSocket(unix_socket=args.host)
        tfactory = TBinaryProtocol.TBinaryProtocolFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        server = TNonblockingServer.TNonblockingServer(processor, transport, tfactory, pfactory)

        collector = PerfCollector(perf_rec_queue, logger)
        collector.setDaemon(True)
        collector.start()

        cfg_path = args.gcfg
        interval = 60.0
        sender = GMetricSender(collector, logger, interval, cfg_path) \
            if cfg_path else PerfSender(collector, logger, interval)
        sender.setDaemon(True)
        sender.start()

        logger.info('Starting the server...')
        server.serve()
        logger.info('done.')
        return

    set_log_dir(args.logdir)
    if args.port:
        log_server = LogRecordTCPSocketReceiver(host=args.host,
                                                port=args.port)
        logger.info("About to start tcp log server with port %s",
                    args.port)
    else:
        log_server = LogRecordUnixSocketReceiver(host=args.host)
        logger.info("About to start unix socket log server"
                    " with socket %s", args.host)

    log_server.serve_until_stopped()
    log_server.server_close()


if __name__ == "__main__":
    main()
