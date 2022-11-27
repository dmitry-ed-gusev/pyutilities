#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Logging config for cmd line utilities.

    Created:  Dmitrii Gusev, 27.11.2022
    Modified:
"""

import os
import logging
import logging.config
from pathlib import Path

logs_dir: str = str(Path.home()) + "/.pyutilities/logs"
encoding: str = "utf-8"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "simple": {  # usually used log format
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },  # end of formatters block
    "handlers": {
        "default": {  # default handler (for emergency cases)
            # "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "console": {  # usual console handler
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "std_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": logs_dir + "/log_info.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 20,
            "encoding": encoding,
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": logs_dir + "/log_errors.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 20,
            "encoding": encoding,
        },
    },  # end of handlers block
    "loggers": {
        "pyutilities": {
            # 'handlers': ['default'],
            "level": "DEBUG",
            # 'propagate': False
        },
        "__main__": {  # if __name__ == '__main__' - emergency case
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        },
    },  # end of loggers module
    "root": {  # root logger
        "level": "DEBUG",
        "handlers": ["console", "std_file_handler", "error_file_handler"],
    },
}


def init_logging():
    # create logs directory
    os.makedirs(str(logs_dir), exist_ok=True)
    # init logging
    logging.config.dictConfig(LOGGING_CONFIG)
    # log message about initialized logger
    logging.getLogger(__name__).debug("Initialized logging.")
