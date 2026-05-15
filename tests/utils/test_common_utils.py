# -*- coding: utf-8 -*-

from itertools import count

import pytest


from pyutilities.utils.common_utils import get_value_safely, myself, build_variations_list
from pyutilities.utils.common_utils import add_kv_2_dict, dict_2_csv


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
