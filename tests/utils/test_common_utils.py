#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for [utils] module from [pyutilities] library.

    Created:  Gusev Dmitrii, 2017
    Modified: Gusev Dmitrii, 12.12.2024
"""

from itertools import count

import pytest

from pyutilities.utils.common_utils import singleton, threadsafe_function, debug_benchmark
from pyutilities.utils.common_utils import get_value_safely
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


@pytest.fixture(name='data_dictionary')
def dictionary():
    yield {"key1": "str_val1", "key2": 100}


def test_get_value_safely(data_dictionary):

    assert get_value_safely(data_dictionary, "key1", "zzz") == "str_val1"
    assert get_value_safely(data_dictionary, "key2", "zzz") == 100
    assert get_value_safely(data_dictionary, "key3", "zzz") == "zzz"
    assert get_value_safely(data_dictionary, "key4", 500) == 500


@pytest.mark.parametrize("data_dict, key, default, expected", [({}, "key1", 500, 500),
                                                               (None, "key2", "asdf", "asdf")])
def test_get_value_safely_empty_dict(data_dict, key, default, expected):

    assert get_value_safely(data_dict, key, default) == expected
