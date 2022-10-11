#!/usr/bin/env python
# coding=utf-8

"""

    Internal exception for pyutilities library.

    Created:  Dmitrii Gusev, 17.05.2019
    Modified: Dmitrii Gusev, 11.10.2022

"""

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE


class PyUtilitiesException(Exception):
    """Custom Scraper exception for various internal exceptions."""
    pass


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
