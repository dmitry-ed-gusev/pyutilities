#!/usr/bin/env python
# coding=utf-8

"""

    Internal exception for pyutilities library.

    Created:  Dmitrii Gusev, 17.05.2019
    Modified:

"""


class PyUtilsException(Exception):

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):  # string representation for print() etc.
        return repr(self.msg)
