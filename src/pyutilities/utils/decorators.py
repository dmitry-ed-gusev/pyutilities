# -*- coding: utf-8 -*-

"""
Decorators module. Contains some useful decorators.

Created:  Gusev Dmitrii, 10.10.2022
Modified: Dmitrii Gusev, 15.05.2026
"""

import functools
import logging
import threading
import time
from typing import Any

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def singleton_v1(clazz):
    """Decorator: singleton class decorator. Use it on the class level to make class Singleton.
    Version 1: uses set of instances for storing the one class instance.
    """

    instances = {}  # classes instances storage

    @functools.wraps(clazz)
    def get_instance(*args, **kwargs):
        if clazz not in instances:
            instances[clazz] = clazz(*args, **kwargs)
        return instances[clazz]

    return get_instance


def singleton_v2(clazz):
    """Decorator: singleton class decorator. Use it on the class level to make class Singleton.
    Version 2: uses reference to the singleton instance for storing the lnk to the one class instance.
    """

    @functools.wraps(clazz)
    def wrapper_singleton(*args, **kwargs):
        if wrapper_singleton.instance is None:  # type: ignore[attr-defined]
            wrapper_singleton.instance = clazz(*args, **kwargs)  # type: ignore[attr-defined]
        return wrapper_singleton.instance  # type: ignore[attr-defined]

    wrapper_singleton.instance = None  # type: ignore[attr-defined]

    return wrapper_singleton


def threadsafe_function(fn):
    """Decorator: it is making sure that the decorated function is thread safe."""

    lock = threading.Lock()  # acquire lock

    @functools.wraps(fn)
    def new(*args, **kwargs):
        with lock:
            result = fn(*args, **kwargs)
        return result

    return new


def debug_benchmark(func):
    """Decorator: logs the given function execution time."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t = time.process_time()
        res = func(*args, **kwargs)
        log.debug("Function [%s] executed in [%s] second(s).", func.__name__, time.process_time() - t)
        return res

    return wrapper


def debug_function_name(func):
    """Decorator: logs the name of the decorating function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log.debug("Function [%s] is working.", func.__name__)
        # print(func.__name__, args, kwargs)
        res = func(*args, **kwargs)
        return res

    return wrapper


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
    """Cache decorator - analogue for the functool.lru_cache().
    WARNING! Unbounded cache!
    """

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


def check_not_none(*arg_names):
    """
    A decorator that checks if specified arguments are not None.

    Args:
        *arg_names: Variable number of strings representing the names of
                    arguments to check for None values.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get the argument names from the function signature
            func_arg_names = func.__code__.co_varnames[: func.__code__.co_argcount]

            # Map positional arguments to their names
            arg_map = dict(zip(func_arg_names, args))
            # Add keyword arguments
            arg_map.update(kwargs)

            for name in arg_names:
                if name not in arg_map:
                    raise TypeError(f"Argument '{name}' not found in function signature.")
                if arg_map[name] is None:
                    raise ValueError(f"Argument '{name}' cannot be None.")
            return func(*args, **kwargs)

        return wrapper

    return decorator


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
