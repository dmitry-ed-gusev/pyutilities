#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for strings module.

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 25.11.2022
"""

import pytest
import unittest
from hypothesis import given
from hypothesis.strategies import characters, text
from pyutilities.utils.string_utils import trim_to_none, trim_to_empty, filter_str, process_url

# common constants for testing
EMPTY_STRINGS = ["", "     ", None, "", "  "]
NON_EMPTY_STRINGS = {"str1": "   str1", "str2": "str2    ", "str3": "   str3     ", "str4": "str4"}


class StringsTest(unittest.TestCase):
    def setUp(self):
        # method just for the demo purpose
        pass

    def tearDown(self):
        # method just for the demo purpose
        pass

    @classmethod
    def setUpClass(cls):
        # method just for the demo purpose
        pass

    @classmethod
    def tearDownClass(cls):
        # method just for the demo purpose
        pass

    def test_trim_to_none_with_empty_strings(self):
        for s in EMPTY_STRINGS:
            self.assertIsNone(trim_to_none(s), "Must be NoNe!")

    def test_trim_to_none_with_non_empty_strings(self):
        for k, v in NON_EMPTY_STRINGS.items():
            self.assertEqual(k, trim_to_none(v), "Must be equals!")

    def test_trim_to_empty_with_empty_strings(self):
        for s in EMPTY_STRINGS:
            self.assertEqual("", trim_to_empty(s), "Must be an empty string!")
            self.assertEqual("", trim_to_empty(s), "Must be an empty string!")

    def test_trim_to_empty_with_non_empty_strings(self):
        for k, v in NON_EMPTY_STRINGS.items():
            self.assertEqual(k, trim_to_empty(v), "Must be equals!")

    def test_filter_str_for_empty(self):
        for string in ["", "    ", None]:
            self.assertEqual(string, filter_str(string))

    def test_filter_str_for_string(self):
        self.assertEqual("45, .555", filter_str("+45, *@.555"))
        self.assertEqual("улица  Правды. 11,", filter_str("улица + =Правды. 11,"))
        self.assertEqual("3-5-7", filter_str("3-5-7"))
        self.assertEqual("zzzz. , fgh ", filter_str("zzzz. ??, fgh *"))


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
        ("http://myurl{}/suburl{}/{}", "", ("aaa", "bbb", "ccc", "www"), "http://myurlaaa/suburlbbb/ccc"),
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


# todo: https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.text
# todo: https://en.wikipedia.org/wiki/Unicode_character_property
@given(
    text(
        alphabet=characters(
            blacklist_categories=(
                "Cc",
                "Zs",
                "Zl",
                "Zp",
            )
        ),
        min_size=1,
        max_size=100,
    )
)
def test_trim_to_none_with_meaningful_symbols(text):
    assert trim_to_none(text) == text


@given(
    text(
        alphabet=characters(
            whitelist_categories=(
                "Zs",
                "Zl",
                "Zp",
            )
        ),
        min_size=1,
        max_size=100,
    )
)
def test_trim_to_none_with_only_non_meaningful_symbols(text):
    assert trim_to_none(text) is None


@given(
    text(
        alphabet=characters(
            blacklist_categories=(
                "Cc",
                "Zs",
                "Zl",
                "Zp",
            )
        ),
        min_size=1,
        max_size=100,
    )
)
def test_trim_to_empty_with_meaningful_symbols(text):
    assert trim_to_empty(text) == text


@given(
    text(
        alphabet=characters(
            whitelist_categories=(
                "Zs",
                "Zl",
                "Zp",
            )
        ),
        min_size=1,
        max_size=100,
    )
)
def test_trim_to_empty_with_only_non_meaningful_symbols(text):
    assert trim_to_empty(text) == ""
