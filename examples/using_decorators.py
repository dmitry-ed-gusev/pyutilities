# -*- coding: utf-8 -*-

"""
Samples for decorators module.

Created:  Dmitrii Gusev, 25.11.2025
Modified: Dmitrii Gusev, 25.11.2025
"""

import time
import datetime
from functools import cache

import requests

from pyutilities.utils.decorators import retry, memoize, timing_decorator, log_execution


@retry(max_tries=5, delay_seconds=2)
def call_dummy_api():
    response = requests.get("https://jsonplaceholder.typicode.ccom/todos/1")
    return response


def fibonacci_no_cache(n):
    if n <= 1:
        return n
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


@cache
def fibonacci_with_cache(n):
    if n <= 1:
        return n
    return fibonacci_with_cache(n - 1) + fibonacci_with_cache(n - 2)


@memoize
def fibonacci_with_memoize(n):
    if n <= 1:
        return n
    return fibonacci_with_memoize(n - 1) + fibonacci_with_memoize(n - 2)


@timing_decorator
def my_function():
    time.sleep(1)  # simulate some time-consuming operation


@log_execution
def extract_data():
    # extract data from source
    data = "some data"
    return data


if __name__ == '__main__':

    print('Samples running...')

    # -- Sample #1 - @retry
    # print(call_dummy_api())

    # -- Sample #2 - no cache/@cache/@memoize
    # FIBONACCI_FOR_NUMBER = 40
    # print(f"\n-- Execution fibonacci function variants ({FIBONACCI_FOR_NUMBER=}):")
    # # ----------
    # print('\n- Start time:', str(start := datetime.datetime.now()))
    # print("\tresult (no cache) = ", fibonacci_no_cache(FIBONACCI_FOR_NUMBER))
    # print('- End time:', str(finish := datetime.datetime.now()))
    # print('- Working time:', str(finish - start))
    # # ----------
    # print('\n- Start time:', str(start := datetime.datetime.now()))
    # print("\tresult (with cache) = ", fibonacci_with_cache(FIBONACCI_FOR_NUMBER))
    # print('- End time:', str(finish := datetime.datetime.now()))
    # print('- Working time:', str(finish - start))
    # # ----------
    # print('\n- Start time:', str(start := datetime.datetime.now()))
    # print("\tresult = ", fibonacci_with_memoize(FIBONACCI_FOR_NUMBER))
    # print('- End time:', str(finish := datetime.datetime.now()))
    # print('- Working time:', str(finish - start))

    # -- Sample #3 - @timing_decorator
    my_function()

    # -- Sample #4 - @log_execution
    extract_data()
