#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Internal exception for pyutilities library.

Created:  Dmitrii Gusev, 17.05.2019
Modified: Dmitrii Gusev, 02.01.2025
"""

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE


class PyUtilitiesException(Exception):
    """Custom exception for [pyutilities] library."""


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
