# -*- coding: utf-8 -*-

import time
import datetime
import requests
from pyutilities.utils.decorators import retry, memoize, timing_decorator


@retry(max_tries=5, delay_seconds=2)
def call_dummy_api():
    response = requests.get("https://jsonplaceholder.typicode.ccom/todos/1")
    return response


def fibonacci_no_cache(n):
    if n <= 1:
        return n
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


@memoize
def fibonacci_with_cache(n):
    if n <= 1:
        return n
    return fibonacci_with_cache(n - 1) + fibonacci_with_cache(n - 2)


@timing_decorator
def my_function():
    # some code here
    time.sleep(1)  # simulate some time-consuming operation
    return


if __name__ == '__main__':

    print('Samples running...')

    # -- Sample #1 - @retry
    # print(call_dummy_api())

    # -- Sample #2 - @memoize
    print("-- Execution without decorator:")
    start = datetime.datetime.now()
    print('- Start time:', str(start))
    print(fibonacci_no_cache(40))
    finish = datetime.datetime.now()
    print('- End time:', str(finish))
    print('- Working time:', str(finish - start))

    print("-- Execution with decorator:")
    start = datetime.datetime.now()
    print('- Start time:', str(start))
    print(fibonacci_with_cache(40))
    finish = datetime.datetime.now()
    print('- End time:', str(finish))
    print('- Working time:', str(finish - start))

    # -- Sample #3 - 
