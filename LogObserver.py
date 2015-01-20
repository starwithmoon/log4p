__author__ = 'root'
#coding:utf-8
from ObserverModel import Subject, Observer
from LogSubject import LogSubject
from pyetc import load, reload, unload

import os
import sys
import logging
import logging.handlers

# Color escape string
COLOR_RED='\033[1;31m'
COLOR_GREEN='\033[1;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[1;34m'
COLOR_PURPLE='\033[1;35m'
COLOR_CYAN='\033[1;36m'
COLOR_GRAY='\033[1;37m'
COLOR_WHITE='\033[1;38m'
COLOR_RESET='\033[1;0m'

# Define log color
LOG_COLORS = {
    'DEBUG': '%s',
    'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
    'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
    'ERROR': COLOR_RED + '%s' + COLOR_RESET,
    'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
    'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
    }

# Global logger
logSubject = LogSubject()
__all__ = ['set_logger', 'debug', 'info', 'warning', 'error',
           'critical', 'exception']

class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''

    def __init__(self, fmt = None, datefmt = None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)

        return LOG_COLORS.get(level_name, '%s') % msg

class log():
    g_logger = None
    config = None
    """
     观察者类
    """
    def __init__(self, module_name="", filename = None, mode = 'a', level='ERROR:DEBUG',
        fmt = '[%(levelname)s] %(asctime)s %(message)s',
        backup_count = 5, limit = 20480, when = None):
        '''Configure the global logger.'''
        global logSubject
        LogObserver = Observer(logSubject)
        LogObserver.update = self.update
        #config = LogObserver.data
        level = level.split(':')

        if len(level) == 1: # Both set to the same level
            s_level = f_level = level[0]
        else:
            s_level = level[0]  # StreamHandler log level
            f_level = level[1]  # FileHandler log level

        self.init_logger(module_name)
        self.add_streamhandler(s_level, fmt)
        self.add_filehandler(f_level, fmt, filename, mode, backup_count, limit, when)

    def update(self, data):
        self.config = data
        level = logging.CRITICAL
        if self.config.has_key("loggers") and self.config.config['loggers'].has_key(""):
            level = self.config.config['loggers']['xxx']['level']
        self.g_logger.setLevel(level)

    def add_handler(self, cls, level, fmt, colorful, **kwargs):
        '''Add a configured handler to the global logger.'''

        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.DEBUG)

        handler = cls(**kwargs)
        handler.setLevel(level)

        if colorful:
            formatter = ColoredFormatter(fmt)
        else:
            formatter = logging.Formatter(fmt)

        handler.setFormatter(formatter)
        self.g_logger.addHandler(handler)

        return handler

    def add_streamhandler(self,level, fmt):
        '''Add a stream handler to the global logger.'''
        return self.add_handler(logging.StreamHandler, level, fmt, True)

    def add_filehandler(self, level, fmt, filename , mode, backup_count, limit, when):
        '''Add a file handler to the global logger.'''
        kwargs = {}

        # If the filename is not set, use the default filename
        if filename is None:
            filename = getattr(sys.modules['__main__'], '__file__', 'log.py')
            filename = os.path.basename(filename.replace('.py', '.log'))
            filename = os.path.join('/tmp', filename)

        kwargs['filename'] = filename

        # Choose the filehandler based on the passed arguments
        if backup_count == 0: # Use FileHandler
            cls = logging.FileHandler
            kwargs['mode' ] = mode
        elif when is None:  # Use RotatingFileHandler
            cls = logging.handlers.RotatingFileHandler
            kwargs['maxBytes'] = limit
            kwargs['backupCount'] = backup_count
            kwargs['mode' ] = mode
        else: # Use TimedRotatingFileHandler
            cls = logging.handlers.TimedRotatingFileHandler
            kwargs['when'] = when
            kwargs['interval'] = limit
            kwargs['backupCount'] = backup_count

        return self.add_handler(cls, level, fmt, False, **kwargs)

    def init_logger(self, module):
        '''Reload the global logger.'''
        if self.g_logger is None:
            if module == "":
                self.g_logger = logging.getLogger()
            else:
                self.g_logger = logging.getLogger(module)
        #else:
        #    logging.shutdown()
        #    self.g_logger.handlers = []

        self.g_logger.setLevel(logging.DEBUG)

    def set_logger(self, module_name="", filename = None, mode = 'a', level='ERROR:DEBUG',
        fmt = '[%(levelname)s] %(asctime)s %(message)s',
        backup_count = 5, limit = 20480, when = None):
        '''Configure the global logger.'''
        level = level.split(':')

        if len(level) == 1: # Both set to the same level
            s_level = f_level = level[0]
        else:
            s_level = level[0]  # StreamHandler log level
            f_level = level[1]  # FileHandler log level

        self.init_logger(module_name)
        self.add_streamhandler(s_level, fmt)
        self.add_filehandler(f_level, fmt, filename, mode, backup_count, limit, when)

    def critical(self, msg):
        self.g_logger.critical(msg)

    def error(self, msg):
        self.g_logger.error(msg)

    def warning(self, msg):
        self.g_logger.warning(msg)

    def info(self, msg):
        self.g_logger.info(msg)

    def debug(self, msg):
        self.g_logger.debug(msg)
