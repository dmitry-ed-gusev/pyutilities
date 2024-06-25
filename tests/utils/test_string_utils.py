#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for strings module.

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 25.06.2024
"""

import pytest

from hypothesis import given
from hypothesis.strategies import characters, text

from pyutilities.utils.string_utils import filter_str, process_url, trim_to_empty, trim_to_none

# common constants for testing
EMPTY_STRINGS = ["", "     ", None, "", "  "]
NON_EMPTY_STRINGS = {
    "str1": "   str1",
    "str2": "str2    ",
    "str3": "   str3     ",
    "str4": "str4",
}


def test_trim_to_none_with_empty_strings():
    for s in EMPTY_STRINGS:
        assert trim_to_none(s) is None, "Must be NoNe!"


def test_trim_to_none_with_non_empty_strings():
    for k, v in NON_EMPTY_STRINGS.items():
        assert k == trim_to_none(v), "Must be equals!"


def test_trim_to_empty_with_empty_strings():
    for s in EMPTY_STRINGS:
        assert "" == trim_to_empty(s), "Must be an empty string!"


def test_trim_to_empty_with_non_empty_strings():
    for k, v in NON_EMPTY_STRINGS.items():
        assert k == trim_to_empty(v), "Must be equals!"


def test_filter_str_for_empty():
    for s in EMPTY_STRINGS:
        assert s == filter_str(s)


def test_filter_str_for_non_empty_strings():
    assert "45, .555" == filter_str("+45, *@.555")
    assert "улица  Правды. 11," == filter_str("улица + =Правды. 11,")
    assert "3-5-7" == filter_str("3-5-7")
    assert "zzzz. , fgh " == filter_str("zzzz. ??, fgh *")


@pytest.mark.parametrize(
    "url, postfix, format_params, expected",
    [
        ("http://myurl/", "123456", None, "http://myurl/123456"),
        ("http://myurl", "123456", None, "http://myurl/123456"),
        ("http://myurl{}/suburl/", "", ("xxx",), "http://myurlxxx/suburl/"),
        ("http://myurl{}/suburl/", "", ("xxx", "zzz"), "http://myurlxxx/suburl/"),
        (
            "http://myurl{}/suburl{}/{}",
            "",
            (
                "aaa",
                "bbb",
                "ccc",
            ),
            "http://myurlaaa/suburlbbb/ccc",
        ),
        (
            "http://myurl{}/suburl{}/{}",
            "",
            ("aaa", "bbb", "ccc", "www"),
            "http://myurlaaa/suburlbbb/ccc",
        ),
        (
            "http://myurl{}/suburl{}/{}",
            "2",
            (
                "_a",
                "_b",
                "_c",
            ),
            "http://myurl_a/suburl_b/_c/2",
        ),
    ],
)
def test_process_url(url, postfix, format_params, expected):
    assert process_url(url, postfix, format_params) == expected


# see info here: https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.text
@given(text(alphabet=characters(blacklist_categories=["Cc", "Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim_to_none_with_meaningful_symbols(text):
    assert trim_to_none(text) == text


@given(text(alphabet=characters(whitelist_categories=["Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim_to_none_with_only_non_meaningful_symbols(text):
    assert trim_to_none(text) is None


@given(text(alphabet=characters(blacklist_categories=["Cc", "Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim_to_empty_with_meaningful_symbols(text):
    assert trim_to_empty(text) == text


@given(text(alphabet=characters(whitelist_categories=["Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim_to_empty_with_only_non_meaningful_symbols(text):
    assert trim_to_empty(text) == ""
