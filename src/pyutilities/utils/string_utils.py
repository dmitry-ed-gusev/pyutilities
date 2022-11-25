#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Some useful/convenient string functions (sometimes - similar
    to module String in java library Apache Commons).

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 25.11.2022
"""

import logging
from typing import Tuple, Dict
from pyutilities.exception import PyUtilitiesException
from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

SPECIAL_SYMBOLS = ".,/-№"
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

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
    return "".join(
        char
        for char in string
        if char.isalnum() or char.isspace() or char in SPECIAL_SYMBOLS or char in CYRILLIC_SYMBOLS
    )


def process_url(url: str, postfix: str = "", format_values: Tuple[str] | None = None) -> str:
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
    log.debug("Processing urls dictionary.")

    if not urls:
        raise PyUtilitiesException("Provided empty URLs dictionary for processing!")

    processed: Dict[str, str] = dict()
    for key in urls:
        processed[key] = process_url(urls[key], postfix, format_values)

    return processed


def get_last_part_of_the_url(url: str) -> str:
    log.debug(f"Calculating the last right part of the URL: [{url}].")

    if not url:  # fail-fast behaviour
        raise PyUtilitiesException("Specified empty URL!")

    return url[url.rfind("/") + 1 :]


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
