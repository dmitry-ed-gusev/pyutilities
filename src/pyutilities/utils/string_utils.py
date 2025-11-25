#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Some useful/convenient string functions (sometimes - similar to module String in java library Apache
Commons). For some functions added one default parameter trace=False, as these functions may be used
in 'fast' executing code, where logging will just add additional complexity and decrease speed.

Also most of the functions use LRU feature of the python language.

Created:  Dmitrii Gusev, 15.04.2019
Modified: Dmitrii Gusev, 23.11.2025
"""

import logging
from functools import cache
from re import match as re_match
from typing import Any, Dict, Iterable, Tuple

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

# configure logger on module level. it isn't a good practice, but it's convenient.
# ! don't forget to set disable_existing_loggers=False, otherwise logger won't get its config!
log = logging.getLogger(__name__)
# to avoid errors like 'no handlers' for libraries it's necessary/convenient to add NullHandler
log.addHandler(logging.NullHandler())

# useful module defaults
SPECIAL_SYMBOLS = ".,/-№"
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
LATIN_SYMBOLS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALL_SYMBOLS = SPECIAL_SYMBOLS + CYRILLIC_SYMBOLS + LATIN_SYMBOLS

# set of regex for determining float values
REGEX_FLOAT_1 = "^\d+?\.\d+?$"  # original regex # pylint: disable=anomalous-backslash-in-string # noqa: W605
REGEX_FLOAT_2 = "^\\d+?\\.\\d+?$"  # original regex with fixed warnings
REGEX_FLOAT_3 = "^[+-]?([0-9]*[.])?[0-9]+$"  # simplified regex, matches: 123/123.456/.456
REGEX_FLOAT_4 = "^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$"  # matches as previous plus: 123.


@cache
def trim_2_none(string: str | None, trace: bool = False) -> str | None:
    """Trim the provided string to None (if empty) or just strip leading/trailing whitespaces."""

    if string and string.strip():  # string isn't empty - trimming whitespaces
        result = string.strip()
    else:  # string is empty - returning None
        result = None

    if trace:  # in case debug enabled - logging function usage
        log.debug("trim_2_none(): input string: [%s], result string: [%s].", string, result)

    return result


@cache
def trim_2_empty(string: str | None, trace: bool = False) -> str:
    """Trim the provided string to empty string - '' or "" - (if empty) or just strip whitespaces."""

    if string and string.strip():  # string isn't empty - trimming whitespaces
        result = string.strip()
    else:  # string is empty
        result = ""

    if trace:
        log.debug("trim_2_empty(): input string: [%s], result string: [%s].", string, result)

    return result


@cache
def filter_str(string: str | None, trace: bool = False):
    """Filter out all unnecessary/unwanted symbols from string (clear string) except letters, numbers,
    spaces, commas. By default, decode input string in unicode (utf-8)."""

    def accepted(char) -> bool:  # internal function
        """Simple internal helper function."""
        return char.isalnum() or char.isspace() or char in ALL_SYMBOLS

    if not string or not string.strip():  # if empty, return input string 'as is'
        result = string
    else:  # string isn't empty - filter out all, except symbols/letters, spaces, or comma
        result = "".join(char for char in string if accepted(char))

    if trace:
        log.debug("filter_str(): filtering string: [%s], result: [%s].", string, result)

    return result


@cache
def process_url(
    url: str, postfix: str = "", format_values: Tuple[str] | None = None, trace: bool = False
) -> str:
    """Process the provided url and update it: add postfix (if provided) and add format values
    (if provided). In case empty string provided = empty string will be returned as well."""

    result: str = ""
    if url and url.strip():  # provided url is not empty

        processed_url: str = url  # processing URL postfix
        if postfix and postfix.strip():  # if postfix isn't empty - add it to the URL string
            if not processed_url.endswith("/"):
                processed_url += "/"
            processed_url += postfix.strip()

        # processing URL format values
        if format_values:  # if there are values - format URL string with them
            processed_url = processed_url.format(*format_values)

        result = processed_url

    if trace:  # trace output
        log.debug(
            "process_url(): URL [%s], postfix [%s], format values [%s].\n\t Result: [%s].",
            url,
            postfix,
            format_values,
            result,
        )

    return result


@cache
def process_urls(
    urls: Dict[str, str], postfix: str = "", format_values: Tuple[str] | None = None, trace: bool = False
) -> Dict[str, str]:
    """Process the provided dictionary of urls with the function"""

    processed: Dict[str, str] = {}

    if urls and len(urls) > 0:  # non-empty urls list for processing
        for key in urls:
            processed[key] = process_url(urls[key], postfix, format_values, trace=trace)

    if trace:  # trace output
        log.debug("process_urls(): urls dict: [%s], result: [%s].", urls, processed)

    return processed


@cache
def get_str_ending(string: str, symbol: str = "/", trace: bool = False) -> str:
    """Returns the last right part of the string after the symbol (not including the symbol itself). It is
    most right part of the string, after the last right symbol (if there are multiple symbols).
    """

    result: str = string

    if (string and string.strip()) and (symbol and symbol.strip()):  # string and symbol both are not empty
        # fmt: off
        result = string[string.rfind(symbol.strip()) + 1:]  # processing string
        # fmt: on

    if trace:  # trace output
        log.debug("get_str_ending(): string: [%s], symbol: [%s], result: [%s].", string, symbol, result)

    return result


@cache
def is_number(value: str, trace: bool = False) -> bool:
    """Returns True if string is a number. String is checked 'as is' - no trailing/leading spaces cut, no
    any other transformations."""

    result: bool = False

    # if match with regex or integrated isdigit() is True - result is True
    if (value and value.strip()) and ((re_match(REGEX_FLOAT_4, value) is not None) or (value.isdigit())):
        result = True

    if trace:
        log.debug("is_number(): input [%s], result [%s].", value, result)

    return result


def iter_2_str(values: Iterable[Any], braces: bool = True, trace: bool = False) -> str:  # noqa: C901
    """Convert number of iterable values to a single string value. If iterable is empty - the result is
    empty string. If braces == True, the braces will be added around the resulting string. For each value
    in the iterable trailing/leading spaces will be cut, duplicates will be removed, duplicate numbers
    will be removed as well."""

    # setup for processing
    resulting_value: str = ""

    resulting_values: set[str] = set()
    check_values: set[float] = set()

    if values:  # provided non-empty iterable

        # processing iterable with values
        for value in values:
            if not (value and str(value).strip()):  # skip empty value
                continue

            # pre-process value - convert int to float for comparison
            str_value: str = str(value).strip()
            should_add_2_result: bool = True  # by default add all string values to result
            if is_number(str_value, trace=trace):  # check number (string representation) for uniqueness
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

    if trace:
        log.debug("iter_2_str(): resulting string is [%s].", resulting_value)

    return resulting_value  # returning result


@cache
def coalesce(*args, trace: bool = False) -> str:
    """Return first not None and not empty value from provided args list."""

    result: str = ""

    if args:  # provided non-empty args

        for arg in args:  # iterate over provided args
            if arg is not None:  # we've found something that is not None (but maybe empty!)
                if isinstance(arg, str):
                    if arg and arg.strip():
                        result = arg.strip()
                        break  # we've found the first result - break
                else:
                    result = str(arg)
                    break  # we've found the first result - break

    if trace:
        log.debug("coalesce(): input [%s], result [%s].", *args, result)

    return result


@cache
def one_of_2_str(string1: str | None, string2: str | None, trace: bool = False) -> str | None:
    """Function returning one of two strings, if other is empty. If both are empty or filled in - method
    returns None (empty value)."""

    result: str | None = None
    if string1 and string1.strip():  # first string check
        if not string2 or not string2.strip():
            result = string1.strip()
    elif string2 and string2.strip():  # second string check
        if not string1 or not string1.strip():
            result = string2.strip()

    if trace:  # trace output
        log.debug("one_of_2_str(): selecting from strings: [%s], [%s] -> [%s].", string1, string2, result)

    return result


@cache
def convert_bytes(num: float, trace: bool = False) -> str:
    """Function will convert bytes to MB.... GB... etc. for readability."""

    # processing of the value
    result: str = "unknown"
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            result = "%3.1f %s" % (num, x)  # pylint: disable=consider-using-f-string
        num /= 1024.0

    if trace:
        log.debug("convert_bytes(): input string [%s], result [%s].", num, result)

    return result


@cache
def str_2_bool(string: str | None, trace: bool = False) -> bool:
    """Convert string to bool. If empty string - return False. If string is not empty - return if string,
    converted to lower case, contains in the list: 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly',
    'uh-huh'."""

    result: bool
    if not string or not string.strip():  # empty string - returning False
        result = False
    else:
        result = string.strip().lower() in [
            "true",
            "1",
            "t",
            "y",
            "yes",
            "yeah",
            "yup",
            "certainly",
            "uh-huh",
        ]

    if trace:
        log.debug("str_2_bool(): input string [%s], result [%s].", string, result)

    return result


@cache
def str_2_int(string: str | None, trace: bool = False) -> int:
    """Convert string to integer number. Empty string or string with non-digit symbols will return 0,
    otherwise will return int(string)."""

    result: int
    if not string or not string.strip():  # empty input string
        result = 0
    else:  # input string isn't empty
        try:
            # extended conversion of values:
            # 1. strip() + replace ',' -> '.' (in order to parse float)
            # 2. parse float value
            # 3. convert int to float - just throw away partial part
            result = int(float(string.strip().replace(",", ".")))
        except ValueError:
            result = 0

    if trace:  # trace output
        log.debug("str_2_int(): input [%s], result [%s].", string, result)

    return result


@cache
def str_2_float(string: str | None, trace: bool = False) -> float:
    """Convert string to float number. Empty string or string with non-digit symbols
    will return 0, otherwise will return float(string)."""

    result: float
    if not string or not string.strip():
        result = 0.0
    else:
        try:
            result = float(string.strip().replace(",", "."))
        except ValueError:
            result = 0.0

    if trace:  # trace output
        log.debug("str_2_float(): input [%s], result [%s].", string, result)

    return result


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
