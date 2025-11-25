# -*- coding: utf-8 -*-

"""
Decorators module. Contains some useful decorators.

Created:  Gusev Dmitrii, 10.10.2022
Modified: Dmitrii Gusev, 25.11.2025
"""

import functools
import logging
import time
from typing import Any

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def retry(max_tries=3, delay_seconds=1):
    """Retrying decorator."""

    def decorator_retry(func):

        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):  # pylint: disable=inconsistent-return-statements
            tries = 0
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # pylint: disable=W0718
                    tries += 1
                    if tries == max_tries:
                        raise e
                    time.sleep(delay_seconds)

        return wrapper_retry

    return decorator_retry


def memoize(func):
    """Decorator - analogue for the functool.lru_cache()."""

    cache: dict[Any, Any] = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]

        result = func(*args)
        cache[args] = result
        return result

    return wrapper


def timing_decorator(func):
    """Execution time measurement decorator."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result

    return wrapper


def log_execution(func):
    """Log function execution decorator."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Executing %s", func.__name__)
        result = func(*args, **kwargs)
        logging.info("Finished executing %s", func.__name__)
        return result

    return wrapper


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
