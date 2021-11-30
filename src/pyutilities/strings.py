#!/usr/bin/env python
# coding=utf-8

"""

    Some useful/convenient string functions (sometimes - similar
    to module String in java library Apache Commons).

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 26.04.2019

"""


def is_str_empty(string):
    """ Check is string empty/NoNe or not.
    :param string:
    :return:
    """
    if string is None:  # check for None
        return True

    if not string or not string.strip():  # check for whitespaces string
        return True

    return False  # all checks passed


def trim_to_none(string):
    """ Trim the provided string to None (if empty) or just strip whitespaces.
    :param string:
    :return:
    """
    if is_str_empty(string):  # check for empty string
        return None

    return string.strip()  # strip and return


def trim_to_empty(string):
    """ Trim the provided string to empty string (''/"") or just strip whitespaces.
    :param string:
    :return:
    """
    if is_str_empty(string):  # check for empty string
        return ''

    return string.strip()


if __name__ == '__main__':
    print("pyutilities.strings: Don't try to execute library as a standalone app!")
