# -*- coding: utf-8 -*-

"""
Decorators module. Contains some useful decorators.

Created:  Gusev Dmitrii, 10.10.2022
Modified: Dmitrii Gusev, 21.07.2025
"""

import functools
import logging
import time
from functools import wraps

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def retry(max_tries=3, delay_seconds=1):

    def decorator_retry(func):

        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            tries = 0
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries += 1
                    if tries == max_tries:
                        raise e
                    time.sleep(delay_seconds)

        return wrapper_retry

    return decorator_retry


# @retry(max_tries=5, delay_seconds=2)
# def call_dummy_api():
#     response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
#     return response


def memoize(func):

    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result

    return wrapper


# @memoize
# def fibonacci(n):
#     if n <= 1:
#         return n
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)


def timing_decorator(func):

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result

    return wrapper


# @timing_decorator
# def my_function():
#     # some code here
#     time.sleep(1)  # simulate some time-consuming operation
#     return


logging.basicConfig(level=logging.INFO)


def log_execution(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finished executing {func.__name__}")
        return result

    return wrapper


# @log_execution
# def extract_data(source):
#     # extract data from source
#     data = ...

#     return data

# @log_execution
# def transform_data(data):
#     # transform data
#     transformed_data = ...

#     return transformed_data

# @log_execution
# def load_data(data, target):
#     # load data into target
#     ...

# def main():
#     # extract data
#     data = extract_data(source)

#     # transform data
#     transformed_data = transform_data(data)

#     # load data
#     load_data(transformed_data, target)

# @log_execution
# @timing_decorator
# def my_function(x, y):
#     time.sleep(1)
#     return x + y
