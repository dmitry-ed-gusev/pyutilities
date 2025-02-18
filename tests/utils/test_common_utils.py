#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for [utils] module from [pyutilities] library.

    Created:  Gusev Dmitrii, 2017
    Modified: Gusev Dmitrii, 12.12.2024
"""

from itertools import count

from pyutilities.utils.common_utils import singleton, threadsafe_function, debug_benchmark
from pyutilities.utils.common_utils import debug_function_name, myself, build_variations_list
from pyutilities.utils.common_utils import add_kv_2_dict, dict_2_csv


def test_singleton():

    @singleton
    class Obj(object):
        _ids = count(0)

        def __init__(self):
            self.id = next(self._ids)

        def get_id(self):
            return self.id

    instance1 = Obj()
    instance2 = Obj()

    assert instance1 == instance2
    assert instance1.id == instance2.id


def test_threadsafe_function():
    # TODO: implement test!
    pass


def test_debug_benchmark():

    @debug_benchmark
    def func_sleep():
        import time
        time.sleep(3)

    func_sleep()


def test_debug_function_name():
    # TODO: implement test!
    pass


def test_myself():
    # TODO: implement test!
    pass


def test_build_variations_list():
    # TODO: implement test!
    pass


def test_add_kv_2_dict():
    # TODO: implement test!
    pass


def test_dict_2_csv():
    # TODO: implement test!
    pass
