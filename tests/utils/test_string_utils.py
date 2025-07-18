#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for strings module.

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 17.07.2025
"""

import math
import pytest
from hypothesis import given
from hypothesis.strategies import characters, text

from pyutilities.utils.string_utils import (coalesce, filter_str, is_number, iter_2_str, process_url,
                                            trim2none, trim2empty, get_str_ending, one_of_2_str,
                                            str_2_bool, str_2_int, str_2_float)

# common constants for testing
EMPTY_STRINGS = ["", "     ", None, "               ", "  "]

NON_EMPTY_STRINGS = {
    "str1": "   str1",
    "str2": "str2    ",
    "str3": "   str3     ",
    "str4": "str4",
}


def test_trim2none_with_empty_strings():
    for s in EMPTY_STRINGS:
        assert trim2none(s) is None, "Must be NoNe!"


def test_trim2none_with_non_empty_strings():
    for k, v in NON_EMPTY_STRINGS.items():
        assert k == trim2none(v), "Must be equals!"


def test_trim2empty_with_empty_strings():
    for s in EMPTY_STRINGS:
        assert "" == trim2empty(s), "Must be an empty string!"


def test_trim2empty_with_non_empty_strings():
    for k, v in NON_EMPTY_STRINGS.items():
        assert k == trim2empty(v), "Must be equals!"


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
def test_trim2none_with_meaningful_symbols(txt):
    assert trim2none(txt) == txt


@given(text(alphabet=characters(whitelist_categories=["Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim2none_with_only_non_meaningful_symbols(text):
    assert trim2none(text) is None


@given(text(alphabet=characters(blacklist_categories=["Cc", "Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim2empty_with_meaningful_symbols(text):
    assert trim2empty(text) == text


@given(text(alphabet=characters(whitelist_categories=["Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim2empty_with_only_non_meaningful_symbols(text):
    assert trim2empty(text) == ""


def test_is_number_usual_values():
    assert is_number("0")
    assert is_number("123")
    assert is_number("123.")
    assert is_number(".456")
    assert is_number("-123.")
    assert is_number("+123.")
    assert is_number("+.456")
    assert is_number("-.456")
    assert is_number("123.000")
    assert is_number("123.456")
    assert is_number("+123.456")
    assert is_number("-123.456")
    assert is_number("+123.000")


def test_is_number_empty_values():
    assert not is_number(None)
    assert not is_number("")
    assert not is_number("      ")


def test_is_number_various_values():
    assert not is_number("asdf")
    assert not is_number("     asdf")
    assert not is_number("asdf     ")
    assert not is_number("e5")


def test_iter_2_str():
    assert iter_2_str(["name"]) == "name"
    assert iter_2_str(("name1", "name2")) == "name1 (name2)"
    assert (iter_2_str(["  \n", "name1", "name2", "name3",
                        "name1", "    "]) == "name1 (name2, name3)")


def test_iter_2_str_no_braces():
    assert iter_2_str(["name"], braces=False) == "name"
    assert iter_2_str(("name1", "name2"), braces=False) == "name1, name2"
    assert (iter_2_str(["  \n", "name1", "name2", "name3",
                        "name1", "    ", ], braces=False) == "name1, name2, name3")


def test_iter_2_str_empty_values():
    assert iter_2_str(None) == ""
    assert iter_2_str("") == ""
    assert iter_2_str([]) == ""
    assert iter_2_str(()) == ""
    assert iter_2_str(["", "       ", ""]) == ""
    assert iter_2_str(["                 ", " \t\t  ", "", "     \n "]) == ""
    assert iter_2_str(("", "        ")) == ""
    assert iter_2_str("      \t\n") == ""


def test_iter_2_str_empty_values_no_braces():
    assert iter_2_str(None, braces=False) == ""
    assert iter_2_str("", braces=False) == ""
    assert iter_2_str([], braces=False) == ""
    assert iter_2_str((), braces=False) == ""
    assert iter_2_str(["", "       ", ""], braces=False) == ""
    assert iter_2_str(["                 ", " \t\t  ", "", "     \n "], braces=False) == ""
    assert iter_2_str(("", "        "), braces=False) == ""
    assert iter_2_str("      \t\n", braces=False) == ""


def test_iter_2_str_duplicates():
    assert iter_2_str(["name", "name", "name"]) == "name"
    assert iter_2_str(["name", "name", "name", "   name", "name      ", "  name      ", " name"]) == "name"


def test_iter_2_str_duplicates_no_braces():
    assert iter_2_str(["name", "name", "name"], braces=False) == "name"
    assert (iter_2_str(["name", "name", "name", "   name", "name      ",
                        "  name      ", " name"], braces=False) == "name")


def test_iter_2_str_values_with_spaces():
    assert iter_2_str(["   name", "name    "]) == "name"
    assert iter_2_str(["   ", "     name    ", "", "name_zzz"]) == "name (name_zzz)"
    assert iter_2_str(("", "  ", "    ", 100, "100-ABC")) == "100 (100-ABC)"


def test_iter_2_str_values_with_spaces_no_braces():
    assert iter_2_str(["   name", "name    "], braces=False) == "name"
    assert iter_2_str(["   ", "     name    ", "", "name_zzz"], braces=False) == "name, name_zzz"
    assert iter_2_str(("", "  ", "    ", 100, "100-ABC"), braces=False) == "100, 100-ABC"


def test_iter_2_str_non_str_values():
    assert iter_2_str([1, 2, 3]) == "1 (2, 3)"
    assert iter_2_str([12, 13]) == "12 (13)"
    assert (iter_2_str(("              \n\t    ", 1.9, 100.000, "    ",
                        23, "    ", None, "ship1")) == "1.9 (100.0, 23, ship1)")


def test_iter_2_str_non_str_values_no_braces():
    assert iter_2_str([1, 2, 3], braces=False) == "1, 2, 3"
    assert iter_2_str([12, 13], braces=False) == "12, 13"
    assert (iter_2_str(("              \n\t    ", 1.9, 100.000, "    ",
                        23, "    ", None, "ship1"), braces=False) == "1.9, 100.0, 23, ship1")


def test_iter_2_str_equal_int_and_float():
    assert iter_2_str([100, 100.0, 100.000]) == "100"
    assert iter_2_str([1, 1.0, 1.000, 1, "1"]) == "1"
    assert iter_2_str([1.0, 1.0000, 1.000, 1, "1"]) == "1.0"
    assert iter_2_str(["1", 1.0, 1.000, 1, "1.0"]) == "1"


def test_coalesce_empty_values():
    assert coalesce("", 0, None) == "0"
    assert coalesce("", None, "0.0") == "0.0"
    assert coalesce("", "    ", None, " ") == ""
    assert coalesce(None) == ""
    assert coalesce("") == ""


def test_coalesce_usual_values():
    assert coalesce(None, "", "asdf", 0.0) == "asdf"
    assert coalesce(None, "0.0", "asdf") == "0.0"
    assert coalesce(None, 100, "asdf", "") == "100"


@pytest.mark.parametrize("string, symbol, expected", [("  ", "/", "  "), ("asdf", " ", "asdf"),
                                                      ("as/df", "/", "df"), ("as/df/gh/hh", "/", "hh"),
                                                      ("asdf/", "/", ""), ("123.4567", ".", "4567")])
def test_get_str_ending(string, symbol, expected):
    assert get_str_ending(string, symbol) == expected


@pytest.mark.parametrize("string1, string2, expected",
                         [("", "", None),
                          ("   ", "", None),
                          ("", "  ", None),
                          ("    ", "      ", None),
                          ("aaa", "bbb", None),
                          ("   aaa", "bbb      ", None),
                          ("  aaaa     ", "        bbb ", None),
                          ("a", "b", None),
                          ("              dfg", "ggg       ", None),
                          ("    fff", "ddd", None),
                          ("eeee    ", "ddd", None),
                          ("   sssss    ", "dddddd ", None),
                          ("    eeee    ", "      rrr", None)])
def test_one_of_2_str_both_empty_or_filled(string1, string2, expected):
    assert one_of_2_str(string1, string2) == expected


@pytest.mark.parametrize("string1, string2, expected",
                         [("aaa", "", "aaa"),
                          ("   aaa", "  ", "aaa"),
                          ("aaa   ", "    ", "aaa"),
                          (" aaa      ", "  ", "aaa"),
                          ("       aaa      ", "", "aaa"),
                          ("", "bbb", "bbb"),
                          ("  ", "   bbb", "bbb"),
                          (" ", "bbb      ", "bbb"),
                          ("        ", "   bbb        ", "bbb"),
                          ("", "   bbb       ", "bbb")])
def test_one_of_2_str_just_one_filled(string1, string2, expected):
    assert one_of_2_str(string1, string2) == expected


@pytest.mark.parametrize("string", EMPTY_STRINGS)
def test_str_2_bool_empty_string(string):
    assert str_2_bool(string) is False


@pytest.mark.parametrize("string", ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh'])
def test_str_2_bool_true(string):
    assert str_2_bool(string) is True


@pytest.mark.parametrize("string", EMPTY_STRINGS)
def test_str_2_int_empty_string(string):
    assert str_2_int(string) == 0


@pytest.mark.parametrize("string, expected", [("10", 10), ("   111   ", 111), ("   -456", -456),
                                              (" +98    ", 98), ("22.5 ", 22), (" -9.0   ", -9),
                                              ("-0  ", 0), ("100,9875    ", 100), ("  001 ", 1),
                                              ("0x000", 0), ("87a99", 0), ("asdf  ", 0)])
def test_str_2_int(string, expected):
    assert str_2_int(string) == expected


@pytest.mark.parametrize("string", EMPTY_STRINGS)
def test_str_2_float_empty_string(string):
    assert math.isclose(str_2_float(string), 0.0, abs_tol=0) is True


@pytest.mark.parametrize("string, expected", [("10,1", 10.1), ("   100  ", 100.0), ("  -98", -98),
                                              ("    555", 555), ("4.123   ", 4.123), ("-9", -9.0),
                                              ("+0.789", 0.789), ("aaa", 0.0), ("   -0.0", 0),])
def test_str_2_float(string, expected):
    assert math.isclose(str_2_float(string), expected, abs_tol=0.0) is True
