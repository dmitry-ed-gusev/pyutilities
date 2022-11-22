#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for strings module.

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 22.11.2022
"""

import pytest
import unittest
from pyutilities.utils.string_utils import filter_str
import pyutilities.utils.string_utils as pystr

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

    def test_is_str_empty_with_empty_strings(self):
        for s in EMPTY_STRINGS:
            self.assertTrue(pystr.is_str_empty(s), "Must be True!")

    def test_is_str_empty_with_non_empty_strings(self):
        for k, v in NON_EMPTY_STRINGS.items():
            self.assertFalse(pystr.is_str_empty(k), "Must be False!")
            self.assertFalse(pystr.is_str_empty(v), "Must be False!")

    def test_trim_to_none_with_empty_strings(self):
        for s in EMPTY_STRINGS:
            self.assertIsNone(pystr.trim_to_none(s), "Must be NoNe!")

    def test_trim_to_none_with_non_empty_strings(self):
        for k, v in NON_EMPTY_STRINGS.items():
            self.assertEqual(k, pystr.trim_to_none(v), "Must be equals!")

    def test_trim_to_empty_with_empty_strings(self):
        for s in EMPTY_STRINGS:
            self.assertEqual("", pystr.trim_to_empty(s), "Must be an empty string!")
            self.assertEqual("", pystr.trim_to_empty(s), "Must be an empty string!")

    def test_trim_to_empty_with_non_empty_strings(self):
        for k, v in NON_EMPTY_STRINGS.items():
            self.assertEqual(k, pystr.trim_to_empty(v), "Must be equals!")

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
    assert pystr.process_url(url, postfix, format_params) == expected
