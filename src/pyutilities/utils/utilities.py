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
    Modified: Dmitrii Gusev, 11.10.2022
"""

import os
import csv
import errno
import logging
import hashlib
import threading
from pathlib import Path
from typing import Dict, List, Tuple, Any
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
        # except Exception as e:
        #     raise e
        finally:
            lock.release()
        return r

    return new


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


def get_last_part_of_the_url(url: str) -> str:
    if not url:  # fail-fast behaviour
        raise PyUtilitiesException("Specified empty URL!")

    return url[url.rfind('/') + 1:]


def add_kv_2_dict(dicts_list: List[Dict[str, str]], kv: Tuple[str, str]):
    """Add specified key-value pair to all dictionaries in the provided dicts list."""
    log.debug(f'add_kv_2_dict(): adding key:value [{kv}] to dicts list.')

    if not dicts_list:
        raise ValueError('Provided empty dictionaries list!')
    if not kv:
        raise ValueError('Provided empty key-value pair!')

    for dictionary in dicts_list:
        dictionary[kv[0]] = kv[1]


def dict_2_csv(dicts_list: List[Dict[str, str]], filename: str, overwrite_file: bool = False):
    """Saving the provided dictionary to the CSV file. If parameter overwrite_file = True -
        the existing file will be overwritten, otherwise existing file will raise an exception.
    """
    log.debug(f'dict_2_csv(): saving the dictionaries list to CSV: [{filename}].')

    if not dicts_list or not filename:  # I - fail-fast check
        raise ValueError(f'Provided empty dictionaries list: [{not dicts_list}] or filename: [{filename}]!')

    if os.path.exists(filename) and not overwrite_file:  # II - file exists and we don't want to overwrite it
        raise PyUtilitiesException(f"File [{filename}] exists but overwrite is [{overwrite_file}]!")

    keys = dicts_list[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dicts_list)


def str_2_file(filename: str, content: str, overwrite_file: bool = False):
    """Write string/text content to the provided file."""
    log.debug(f'str_2_file(): saving content to file: [{filename}].')

    if os.path.exists(filename) and not overwrite_file:  # file exists and we don't want to overwrite it
        raise PyUtilitiesException(f"File [{filename}] exists but overwrite is [{overwrite_file}]!")

    if not os.path.exists(os.path.dirname(filename)):  # create a dir for file
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:  # write content to a file
        f.write(content)


def file_2_str(filename: str) -> str:
    """Read content from the provided file as string/text."""
    log.debug(f'file_2_str(): reading content from file: [{filename}].')

    if not filename:  # fail-fast behaviour (empty path)
        raise PyUtilitiesException("Specified empty file path!")
    if not os.path.exists(os.path.dirname(filename)):  # fail-fast behaviour (non-existent path)
        raise PyUtilitiesException(f"Specified path [{filename}] doesn't exist!")

    with open(filename, mode='r') as infile:
        return infile.read()


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
