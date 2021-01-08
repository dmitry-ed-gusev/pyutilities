#!/usr/bin/env python
# coding=utf-8

"""
    Logging utilities for some convenience.

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 24.05.2019

"""

import os
import yaml
import logging
import inspect
import logging.config
import pyutilities.strings as strings
from pyutilities.pyexception import PyUtilsException

# init module logger. See more info in utils.py
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# handy utility function/lambda for getting name of executing function from inside the function
# myself = lambda: inspect.stack()[1][3]
def myself():
    return inspect.stack()[1][3]


def init_logger(logger_name: str, add_null_handler: bool = True) -> logging.Logger:
    """
    Init logger without any configuration. Also adds dummy handler in order to avoid errors like 'no handlers'.
    :return: logger, initialized by name.
    """
    if not strings.is_str_empty(logger_name):  # init logger if name isn't empty
        tmp_log = logging.getLogger(logger_name)
        if add_null_handler:
            tmp_log.addHandler(logging.NullHandler)  # added dummy handler in order to avoid errors like 'no handlers'
        return tmp_log

    raise PyUtilsException("Empty logger name provided!")


# todo: add init by provided dictionary structure
def setup_logging(default_path='configs/logging.yml', default_level=logging.INFO, env_key='LOG_CFG', logger_name=None):
    """
        Setup logging configuration - load it from YAML file. Default level is INFO. Configuration file name can be
        provided by multiple ways:
          * via function parameter <default_path> - direct value
          * via environment variable <LOG_ENV> - overrides value from <default_path>
        Default value for config file is <configs/logging.yml> - path relative to current working dir.
        :param default_path path to logging config YAML file
        :param default_level default logging level - INFO
        :param env_key environment variable key to override settings from cmd line,
               like LOG_CFG=my_logging_config.yml
        :param logger_name name of the logger, that should be initialized and returned (by this method)
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value

    if os.path.exists(path):  # load config from specified file
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        log.info('Loaded logging config from [{}].'.format(path))
    else:  # use basic (default) config
        logging.basicConfig(level=default_level)
        log.info('Using basic logging config. Can\'t load config from [{}].'.format(path))

    # todo: init logger before loading configuration?
    # todo: should we add NullHandler if we initialize logger?ß
    if logger_name:  # init and return logger
        log.info('Initializing logger [{}].'.format(logger_name))
        return init_logger(logger_name, add_null_handler=False)


if __name__ == '__main__':
    print("pyutilities.pylog: Don't try to execute library as a standalone app!")
