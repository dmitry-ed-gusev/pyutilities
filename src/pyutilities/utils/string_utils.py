#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# cspell:ignore isnt абвгдеёжзийклмнопрстуфхцчшщъыьэюя

"""
    Some useful/convenient string functions (sometimes - similar
    to module String in java library Apache Commons).

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 07.08.2024
"""

import logging
from typing import Dict, Tuple, Iterable
from re import match as re_match

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE
from pyutilities.exception import PyUtilitiesException

# useful module defaults
SPECIAL_SYMBOLS = ".,/-№"
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
LATIN_SYMBOLS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# set of regex for determining float values
REGEX_FLOAT_1 = "^\d+?\.\d+?$"  # original regex
REGEX_FLOAT_2 = "^\\d+?\\.\\d+?$"  # original regex with fixed warnings
REGEX_FLOAT_3 = "^[+-]?([0-9]*[.])?[0-9]+$"  # simplified regex, matches: 123/123.456/.456
REGEX_FLOAT_4 = "^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$"  # matches as previous plus: 123.

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def trim_to_none(string: str | None) -> str | None:
    """Trim the provided string to None (if empty) or just strip whitespaces."""

    if string and string.strip():
        return string.strip()

    return None


def trim_to_empty(string: str | None) -> str:
    """Trim the provided string to empty string ('' or "") or just strip whitespaces."""

    if string and string.strip():
        return string.strip()

    return ""


def filter_str(string):
    """
    Filter out all symbols from string except letters, numbers, spaces, commas.
    By default, decode input string in unicode (utf-8).
    :param string:
    :return:
    """

    if not string or not string.strip():  # if empty, return 'as is'
        return string

    # filter out all, except symbols/letters, spaces, or comma
    return "".join(
        char
        for char in string
        if char.isalnum()
        or char.isspace()
        or char in SPECIAL_SYMBOLS
        or char in CYRILLIC_SYMBOLS
        or char in LATIN_SYMBOLS
    )


def process_url(url: str, postfix: str = "", format_values: Tuple[str] | None = None) -> str:
    """ TBD """

    log.debug(f"Processing URL [{url}] with postfix [{postfix}] and format values [{format_values}].")

    if not url:
        raise PyUtilitiesException("Provided empty URL for processing!")

    processed_url: str = url
    if postfix:  # if postfix - add it to the URL string
        if not processed_url.endswith("/"):
            processed_url += "/"
        processed_url += postfix

    if format_values:  # if there are values - format URL string with them
        processed_url = processed_url.format(*format_values)

    return processed_url


def process_urls(
    urls: Dict[str, str], postfix: str = "", format_values: Tuple[str] | None = None
) -> Dict[str, str]:
    """ TBD """

    log.debug("Processing urls dictionary.")

    if not urls:
        raise PyUtilitiesException("Provided empty URLs dictionary for processing!")

    processed: Dict[str, str] = dict()
    for key in urls:
        processed[key] = process_url(urls[key], postfix, format_values)

    return processed


def get_last_part_of_the_url(url: str) -> str:
    """ TBD """

    log.debug(f"Calculating the last right part of the URL: [{url}].")

    if not url:  # fail-fast behaviour
        raise PyUtilitiesException("Specified empty URL!")

    return url[url.rfind("/") + 1 :]


def is_number(value: str):
    """Returns True if string is a number."""

    if not (value and value.strip()):  # empty value - not a number
        return False
    if re_match(REGEX_FLOAT_4, value) is None:  # no match with regex - check with integrated isdigit()
        return value.isdigit()

    return True  # regex match returned match


def iter_2_str(values: Iterable, braces: bool = True) -> str:
    """Convert number of iterable values to a single string value."""

    if not values:  # empty iterable - return empty string value - ""
        log.warning("iter_2_str(): provided empty iterable!")
        return ""

    # setup for processing
    resulting_value: str = ""
    resulting_values: set[str] = set()
    check_values: set[float] = set()

    # processing iterable with values
    for value in values:
        if not (value and str(value).strip()):  # skip empty value
            continue

        # pre-process value - convert int to float for comparison
        str_value: str = str(value).strip()
        should_add_2_result: bool = True  # by default add all string values to result
        if is_number(str_value):  # check number (string representation) for uniqueness
            len_before = len(check_values)
            check_values.add(float(str_value))
            should_add_2_result = len_before != len(check_values)  # if not unique number - won't add

        if should_add_2_result:  # add string value to the result
            # adding value to the result
            if braces and len(resulting_values) == 0:  # adding the first non-empty value with braces
                resulting_value += str_value + " ("
                resulting_values.add(str_value)
            else:  # adding further names + preventing adding duplicates
                tmp_len = len(resulting_values)
                resulting_values.add(str_value)
                if tmp_len < len(resulting_values):  # if value was added to the set (it's new and unique)
                    resulting_value += str_value + ", "

    # post-processing - adding trailing brace -> ')' - only if any name was added
    if resulting_value and len(resulting_values) > 0:
        if braces and len(resulting_values) > 1:
            resulting_value = resulting_value[:-2] + ")"
        else:
            resulting_value = resulting_value[:-2]

    return resulting_value  # returning result


def coalesce(*args) -> str:
    """Return first not None and not empty value from provided args list."""

    if not args:
        return ""

    for arg in args:
        if arg is not None:
            if isinstance(arg, str):
                if arg and arg.strip():
                    return arg.strip()
            else:
                return str(arg)

    return ""


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
