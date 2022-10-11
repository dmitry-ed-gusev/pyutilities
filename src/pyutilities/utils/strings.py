#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Some useful/convenient string functions (sometimes - similar
    to module String in java library Apache Commons).

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 11.10.2022
"""

import logging
from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

SPECIAL_SYMBOLS = ".,/-№"
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def is_str_empty(string: str) -> bool:
    """Check is string empty/NoNe or not.
    :param string:
    :return:
    """
    if string is None or not string or not string.strip():  # check for whitespaces string
        return True

    return False  # all checks passed


def trim_to_none(string: str):
    """Trim the provided string to None (if empty) or just strip whitespaces.
    :param string:
    :return:
    """
    if is_str_empty(string):  # check for empty string
        return None

    return string.strip()  # strip and return


def trim_to_empty(string: str) -> str:
    """Trim the provided string to empty string (''/"") or just strip whitespaces.
    :param string:
    :return:
    """
    if is_str_empty(string):  # check for empty string
        return ""

    return string.strip()


def filter_str(string):  # todo: fix filtering for non-cyrillic symbols too (add them)
    """
    Filter out all symbols from string except letters, numbers, spaces, commas.
    By default, decode input string in unicode (utf-8).
    :param string:
    :return:
    """
    if not string or not string.strip():  # if empty, return 'as is'
        return string
    # filter out all, except symbols, spaces, or comma
    return "".join(char for char in string if char.isalnum() or
                   char.isspace() or char in SPECIAL_SYMBOLS or char in CYRILLIC_SYMBOLS)


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
