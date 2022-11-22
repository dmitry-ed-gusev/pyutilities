#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Common utilities module.

    Useful materials:
        - (datetime) https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        - (list of dicts to csv)
          https://stackoverflow.com/questions/3086973/how-do-i-convert-this-list-of-dictionaries-to-a-csv-file
        - ???

    Created:  Gusev Dmitrii, 10.10.2022
    Modified: Dmitrii Gusev, 22.11.2022
"""

import os
import csv
import logging
import inspect
import threading
from typing import Dict, List, Tuple
from pyutilities.exception import PyUtilitiesException
from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

# configure logger on module level. it isn't a good practice, but it's convenient.
# don't forget to set disable_existing_loggers=False, otherwise logger won't get its config!
log = logging.getLogger(__name__)
# to avoid errors like 'no handlers' for libraries it's necessary/convenient to add NullHandler
log.addHandler(logging.NullHandler())

# useful module constants
RUS_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ENG_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM_CHARS = "0123456789"
SPEC_CHARS = "-"


def singleton(class_):
    """Simple singleton class decorator. Use it on the class level to make class Singleton."""

    instances = {}  # classes instances storage

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def threadsafe_function(fn):
    """Decorator making sure that the decorated function is thread safe."""
    lock = threading.Lock()

    def new(*args, **kwargs):
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        finally:
            lock.release()
        return r

    return new


def debug_benchmark(func):
    """This decorator logs the given function execution time."""
    import time

    def wrapper(*args, **kwargs):
        t = time.process_time()
        res = func(*args, **kwargs)
        log.debug(f"Function [{func.__name__}] executed in [{time.process_time() - t}] second(s).")
        return res

    return wrapper


def debug_function_name(func):
    """This decorator logs the name of the decorating function."""

    def wrapper(*args, **kwargs):
        log.debug(f"Function [{func.__name__}] is working.")
        # print(func.__name__, args, kwargs)
        res = func(*args, **kwargs)
        return res

    return wrapper


# handy utility function/lambda for getting name of executing function from inside the function
# myself = lambda: inspect.stack()[1][3]
def myself():
    return inspect.stack()[1][3]


# todo: 1. perform the pre-build of the variations and store them in the scraper db
# todo: 2. re-build variations when necessary
def build_variations_list() -> list:
    """Build list of possible variations of symbols for search.
    :return: list of variations
    """
    log.debug("build_variations_list(): processing.")

    result = list()  # resulting list
    for letter1 in RUS_CHARS + ENG_CHARS + NUM_CHARS:
        for letter2 in RUS_CHARS + ENG_CHARS + NUM_CHARS:
            result.append(letter1 + letter2)  # add value to resulting list
            for spec_symbol in SPEC_CHARS:
                result.append(letter1 + spec_symbol + letter2)  # add value to resulting list

    return result


def add_kv_2_dict(dicts_list: List[Dict[str, str]], kv: Tuple[str, str]):
    """Add specified key-value pair to all dictionaries in the provided dicts list."""
    log.debug(f"add_kv_2_dict(): adding key:value [{kv}] to dicts list.")

    if not dicts_list:
        raise ValueError("Provided empty dictionaries list!")
    if not kv:
        raise ValueError("Provided empty key-value pair!")

    for dictionary in dicts_list:
        dictionary[kv[0]] = kv[1]


def dict_2_csv(dicts_list: List[Dict[str, str]], filename: str, overwrite_file: bool = False):
    """Saving the provided dictionary to the CSV file. If parameter overwrite_file = True -
    the existing file will be overwritten, otherwise existing file will raise an exception.
    """
    log.debug(f"dict_2_csv(): saving the dictionaries list to CSV: [{filename}].")

    if not dicts_list or not filename:  # I - fail-fast check
        raise ValueError(f"Provided empty dictionaries list: [{not dicts_list}] or filename: [{filename}]!")

    if os.path.exists(filename) and not overwrite_file:  # II - file exists and we don't want to overwrite it
        raise PyUtilitiesException(f"File [{filename}] exists but overwrite is [{overwrite_file}]!")

    keys = dicts_list[0].keys()
    with open(filename, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dicts_list)


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
