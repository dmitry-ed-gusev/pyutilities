# -*- coding: utf-8 -*-

"""
Common utilities module.

Useful materials:
    - (datetime) https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    - (list of dicts to csv) https://stackoverflow.com/questions/3086973/
        how-do-i-convert-this-list-of-dictionaries-to-a-csv-file

Created:  Gusev Dmitrii, 10.10.2022
Modified: Dmitrii Gusev, 14.05.2026
"""

import csv
import inspect
import logging
import os
from typing import Any, Dict, List, Tuple

from pyutilities.defaults import DEFAULT_ENCODING, MSG_MODULE_ISNT_RUNNABLE
from pyutilities.exception import PyUtilitiesException

# configure logger on module level. it isn't a good practice, but it's convenient.
# ! don't forget to set disable_existing_loggers=False, otherwise logger won't get its config!
log = logging.getLogger(__name__)
# to avoid errors like 'no handlers' for libraries it's necessary/convenient to add NullHandler
log.addHandler(logging.NullHandler())

# useful module constants
RUS_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ENG_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM_CHARS = "0123456789"
SPEC_CHARS = "-"


def myself():
    """Handy utility function/lambda for getting name of executing function from inside the function.
    Can be rewritten as lambda: myself = lambda: inspect.stack()[1][3]"""

    return inspect.stack()[1][3]


def build_variations_list() -> list[Any]:
    """Build list of possible variations of provided symbols.
    :return: list of variations
    """

    log.debug("build_variations_list(): processing.")

    result = []  # resulting list
    for letter1 in RUS_CHARS + ENG_CHARS + NUM_CHARS:
        for letter2 in RUS_CHARS + ENG_CHARS + NUM_CHARS:
            result.append(letter1 + letter2)  # add value to resulting list
            for spec_symbol in SPEC_CHARS:
                result.append(letter1 + spec_symbol + letter2)  # add value to resulting list

    return result


def add_kv_2_dict(dicts_list: List[Dict[str, str]], kv: Tuple[str, str]):
    """Add specified key-value pair to all dictionaries in the provided dicts list."""

    log.debug("add_kv_2_dict(): adding key:value [%s] to dicts list.", kv)

    if not dicts_list:
        raise ValueError("Provided empty dictionaries list!")

    if not kv:
        raise ValueError("Provided empty key-value pair!")

    for dictionary in dicts_list:
        dictionary[kv[0]] = kv[1]


def dict_2_csv(dicts_list: List[Dict[str, str]], filename: str, overwrite_file: bool = False):
    """
    Saving the provided dictionary to the CSV file. If parameter overwrite_file = True -
    the existing file will be overwritten, otherwise existing file will raise an exception.
    """

    log.debug("dict_2_csv(): saving the dictionaries list to CSV: [%s].", filename)

    if not dicts_list or not filename:  # I - fail-fast check
        raise ValueError(f"Provided empty dictionaries list: [{not dicts_list}] or filename: [{filename}]!")

    if os.path.exists(filename) and not overwrite_file:  # II - file exists and we don't want to overwrite it
        raise PyUtilitiesException(f"File [{filename}] exists but overwrite is [{overwrite_file}]!")

    keys = dicts_list[0].keys()
    with open(filename, "w", newline="", encoding=DEFAULT_ENCODING) as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dicts_list)


def get_value_safely(dictionary: dict[str, str | None], key: str, default_value: Any) -> Any:
    """Safely retrieves a value from a dictionary, handling both a potential None dictionary and a
    missing key."""

    if dictionary:
        return dictionary.get(key, default_value)  # The .get() method handles the missing key gracefully

    return default_value  # If the dictionary itself is None, return the default value


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
