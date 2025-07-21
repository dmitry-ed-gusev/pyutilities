# -*- coding: utf-8 -*-

import math
import pytest

from pyutilities.sys.sys_utils import (get_str_from_env, get_int_from_env,
                                       get_float_from_env, get_bool_from_env)

EMPTY_KEYS_LIST = ["", "   ", "        ", None]


def test_get_str_from_env_empty_env():
    assert get_str_from_env("ZZZ") == ""


@pytest.mark.parametrize("string", EMPTY_KEYS_LIST)
def test_get_str_from_env_empty_key(string):
    assert get_str_from_env(string) == ""


def test_get_str_from_env(monkeypatch):
    monkeypatch.setenv("NAME", "value_zzz")
    assert get_str_from_env("NAME") == "value_zzz"


def test_get_int_from_env_empty_env():
    assert get_int_from_env("ZZZ") == 0


@pytest.mark.parametrize("string", EMPTY_KEYS_LIST)
def test_get_int_from_env_empty_key(string):
    assert get_int_from_env(string) == 0


def test_get_int_from_env(monkeypatch):
    monkeypatch.setenv("INT_VALUE", " -987")
    assert get_int_from_env("INT_VALUE") == -987


def test_get_float_from_env_empty_env():
    assert math.isclose(get_float_from_env("ZZZ"), 0.0, abs_tol=0)


@pytest.mark.parametrize("string", EMPTY_KEYS_LIST)
def test_get_float_from_env_empty_key(string):
    assert math.isclose(get_float_from_env(string), 0.0, abs_tol=0)


def test_get_float_from_env(monkeypatch):
    monkeypatch.setenv("FLOAT_VALUE", "  +456,34    ")
    assert math.isclose(get_float_from_env("FLOAT_VALUE"), 456.34, abs_tol=0)


def test_get_bool_from_env_empty_env():
    assert get_bool_from_env("ZZZ") is False


@pytest.mark.parametrize("string", EMPTY_KEYS_LIST)
def test_get_bool_from_env_empty_key(string):
    assert get_bool_from_env(string) is False


def test_get_bool_from_env(monkeypatch):
    monkeypatch.setenv("BOOL_VALUE", " yes   ")
    assert get_bool_from_env("BOOL_VALUE") is True
