#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
    Some useful/convenient string functions (sometimes - similar to module String in java library Apache
    Commons). For some functions added one default parameter debug=False, as these functions may be used
    in 'fast' executing code, where logging will just add additional complexity and decrease speed.

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 18.07.2025
"""

import logging
from re import match as re_match
from typing import Dict, Iterable, Tuple, Any

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE
from pyutilities.exception import PyUtilitiesException

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
REGEX_FLOAT_1 = "^\d+?\.\d+?$"  # original regex
REGEX_FLOAT_2 = "^\\d+?\\.\\d+?$"  # original regex with fixed warnings
REGEX_FLOAT_3 = "^[+-]?([0-9]*[.])?[0-9]+$"  # simplified regex, matches: 123/123.456/.456
REGEX_FLOAT_4 = "^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$"  # matches as previous plus: 123.


def trim2none(string: str | None, debug: bool = False) -> str | None:
    """Trim the provided string to None (if empty) or just strip whitespaces.
    :param string: string for trimming leading/trailing whitespaces.
    :type string: string or None
    :param debug: enable/disable debug output for the function, defaults to False
    :type debug: boolean, optional
    :return: string with trimmed leading+trailing whitespaces or None (in case input - empty string)
    :rtype: string or None
    """

    if string and string.strip():  # string isn't empty - trimming whitespaces
        result = string.strip()
    else:  # string is empty - returning None
        result = None
    if debug:  # in case debug enabled - logging function usage
        log.debug("trim2none(): input string: [%s], result string: [%s].", string, result)
    return result


def trim2empty(string: str | None, debug=False) -> str:
    """Trim the provided string to empty string - '' or "" - (if empty) or just strip whitespaces."""

    if string and string.strip():  # string isn't empty - trimming whitespaces
        result = string.strip()
    else:  # string is empty
        result = ""
    if debug:
        log.debug(f"trim2empty(): input string: [{string}], result string: [{result}].")
    return result


def filter_str(string: str | None, debug=False):
    """Filter out all unnecessary/unwanted symbols from string (clear string) except letters, numbers,
        spaces, commas. By default, decode input string in unicode (utf-8).
    :param string: input string for filtering
    :type string:
    :param debug: on/off internal debug logging
    :type debug:
    :return:
    :rtype:
    """

    def accepted(char) -> bool:  # internal function
        """Simple internal helper function."""
        return char.isalnum() or char.isspace() or char in ALL_SYMBOLS

    if not string or not string.strip():  # if empty, return input string 'as is'
        result = string
    else:  # string isn't empty - filter out all, except symbols/letters, spaces, or comma
        result = "".join(char for char in string if accepted(char))
    if debug:
        log.debug("filter_str(): Filtering string: [%s], result: [result].", string)
    return result


def process_url(url: str, postfix: str = "", format_values: Tuple[str] | None = None, debug=False) -> str:
    """Process the provided url and update it: add postfix (if provided) and add format values (if provided).
    :param url:
    :param postfix:
    :param format_values:
    :return:
    """

    if not url or not url.strip():  # provided url is empty - raise an exception
        raise PyUtilitiesException("Provided empty URL for processing!")
    # processing URL postfix
    processed_url: str = url
    if postfix and postfix.strip():  # if postfix isn't empty - add it to the URL string
        if not processed_url.endswith("/"):
            processed_url += "/"
        processed_url += postfix.strip()
    # processing URL format values
    if format_values:  # if there are values - format URL string with them
        processed_url = processed_url.format(*format_values)
    # debug output
    if debug:
        log.debug("process_url(): URL [%s], postfix [%s], format values [%s].\n\t Result: [%s].",
                  url, postfix, format_values, processed_url)
    return processed_url


def process_urls(urls: Dict[str, str], postfix: str = "",
                 format_values: Tuple[str] | None = None, debug=False) -> Dict[str, str]:
    """Process the provided dictionary of urls with the function"""

    if debug:
        log.debug("process_urls(): processing provided dictionary of urls.")
    if not urls or len(urls) == 0:
        raise PyUtilitiesException("Provided empty URLs dictionary for processing!")
    processed: Dict[str, str] = {}
    for key in urls:
        processed[key] = process_url(urls[key], postfix, format_values, debug)
    return processed


def get_str_ending(string: str, symbol: str = "/", debug: bool = False) -> str:
    """Returns the last right part of the string after the symbol (not including the symbol itself). It is
    most right part of the string, after the last right symbol (if there are multiple symbols).
    """

    if not (string and string.strip()):  # fail-fast behavior - empty string - returns string 'as is'
        if debug:
            log.debug("Provided empty original string, returning the original string 'as is'.")

    if not (symbol and symbol.strip()):  # fast-check - empty symbol - returns the whole string
        if debug:
            log.debug("Provided empty delimiter symbol, returning the original string.")
        return string

    result = string[string.rfind(symbol.strip()) + 1:]  # processing string (string and symbol are not empty)
    if debug:
        log.debug("get_str_ending(): string: [%s], symbol: [%s], result: [%s].", string, symbol, result)

    return result


def is_number(value: str, debug: bool = False):
    """Returns True if string is a number."""

    if not (value and value.strip()):  # empty value - not a number
        return False

    if re_match(REGEX_FLOAT_4, value) is None:  # no match with regex - check with integrated isdigit()
        return value.isdigit()

    return True  # regex match returned match


def iter_2_str(values: Iterable[Any], braces: bool = True, debug: bool = False) -> str:
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


def coalesce(*args, debug: bool = False) -> str:
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


def one_of_2_str(string1: str | None, string2: str | None) -> str | None:
    """Function returning one of two strings, if other is empty. If both are empty or filled in - method
    returns None (empty value)."""

    if string1 and string1.strip():  # first string check
        if not string2 or not string2.strip():
            return string1.strip()

    elif string2 and string2.strip():  # second string check
        if not string1 or not string1.strip():
            return string2.strip()

    # can't select cluster name from alert (both empty or both filled in)
    # logger.warning(f"Can't select one of 2 strings: {string1=}, {string2=}")
    return None


def convert_bytes(num: float) -> str:
    """Function will convert bytes to MB.... GB... etc. for readability."""

    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)  # pylint: disable=consider-using-f-string
        num /= 1024.0

    return "unknown"


def str_2_bool(string: str | None) -> bool:
    """Convert string to bool. If empty string - return False. If string is not empty - return if string,
    converted to lower case, contains in the list: 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly',
    'uh-huh'."""

    if not string or not string.strip():  # empty string - returning False
        return False

    return string.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


def str_2_int(string: str | None) -> int:
    """Convert string to integer number. Empty string or string with non-digit symbols will return 0,
    otherwise will return int(string)."""

    if not string or not string.strip():
        return 0

    try:
        # extended conversion of values:
        # 1. strip() + replace ',' -> '.' (in order to parse float)
        # 2. parse float value
        # 3. convert int to float - just throw away partial part
        return int(float(string.strip().replace(',', '.')))
    except ValueError:
        return 0


def str_2_float(string: str | None) -> float:
    """Convert string to float number. Empty string or string with non-digit symbols will return 0, otherwise
    will return float(string)."""

    if not string or not string.strip():
        return 0.0

    try:
        return float(string.strip().replace(',', '.'))
    except ValueError:
        return 0.0


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
