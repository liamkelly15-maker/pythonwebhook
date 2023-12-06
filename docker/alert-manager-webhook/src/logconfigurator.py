

import logging
import sys


class LogConfigurator:

    def __init__(self):
        self.logger = None
        self.logger = logging.getLogger('eric-pm-alarm-handler-webhook')

    def configure(self, loglevel):
        self.set_level(loglevel)
        log_message_formatter = self.get_log_formatter()
        self.add_handler(log_message_formatter)
        return self.logger

    def set_level(self, loglevel):
        if loglevel.upper() == 'INFO':
            self.logger.setLevel(logging.INFO)
        if loglevel.upper() == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        if loglevel.upper() == 'ERROR':
            self.logger.setLevel(logging.ERROR)

    def get_log_formatter(self):
        return logging.Formatter("ts=%(asctime)s.%(msecs)03d thread=%(threadName)s level=%(levelname)s msg=%(message)s" \
                                 , datefmt='%Y-%m-%dT%H:%M:%S')

    def add_handler(self, log_message_formatter):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(log_message_formatter)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger

