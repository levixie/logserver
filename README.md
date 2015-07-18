# logserver
just a simple python logserver

there are two different implementations
1. simple tcp/unix socket
you can use it to log your python log, you just need to use the common.log_handlers.SimpleSocketHandler
```
slogger.setUpLogger(host=args.logger_host,
                    port=args.logger_port,
                    log_dir=args.logdir,
                    logger_name='myprog',
                    level=args.loglevel)
logger = logging.getLogger('myprog_1')
```
to set your logger


2. simple thrift tcp/unix socket
you can use it to log your python log, you just need to use the common.log_handlers.SimpleThriftHandler
```
slogger.setUpLogger(host=args.logger_host,
                    port=args.logger_port,
                    log_dir=args.logdir,
                    logger_name='myprog',
                    level=args.loglevel)
logger = logging.getLogger('myprog_1')
```
to set your logger

you can use it to log all your other languages log **TODO**

**when the host is a sock file, it works by unix socket**