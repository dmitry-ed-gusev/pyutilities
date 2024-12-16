#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for strings module.

    Created:  Dmitrii Gusev, 15.04.2019
    Modified: Dmitrii Gusev, 14.12.2024
"""

import pytest
from hypothesis import given
from hypothesis.strategies import characters, text

from pyutilities.utils.string_utils import (
    coalesce,
    filter_str,
    is_number,
    iter_2_str,
    process_url,
    trim2none,
    trim2empty,
)

# common constants for testing
EMPTY_STRINGS = ["", "     ", None, "", "  "]
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
def test_trim_to_none_with_meaningful_symbols(txt):
    assert trim_to_none(txt) == txt


@given(text(alphabet=characters(whitelist_categories=["Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim_to_none_with_only_non_meaningful_symbols(text):
    assert trim_to_none(text) is None


@given(text(alphabet=characters(blacklist_categories=["Cc", "Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim_to_empty_with_meaningful_symbols(text):
    assert trim_to_empty(text) == text


@given(text(alphabet=characters(whitelist_categories=["Zs", "Zl", "Zp"]), min_size=1, max_size=100))
def test_trim_to_empty_with_only_non_meaningful_symbols(text):
    assert trim_to_empty(text) == ""


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
    assert (
        iter_2_str(
            [
                "  \n",
                "name1",
                "name2",
                "name3",
                "name1",
                "    ",
            ]
        )
        == "name1 (name2, name3)"
    )


def test_iter_2_str_no_braces():
    assert iter_2_str(["name"], braces=False) == "name"
    assert iter_2_str(("name1", "name2"), braces=False) == "name1, name2"
    assert (
        iter_2_str(
            [
                "  \n",
                "name1",
                "name2",
                "name3",
                "name1",
                "    ",
            ],
            braces=False,
        )
        == "name1, name2, name3"
    )


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
    assert (
        iter_2_str(["name", "name", "name", "   name", "name      ", "  name      ", " name"], braces=False)
        == "name"
    )


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
    assert (
        iter_2_str(("              \n\t    ", 1.9, 100.000, "    ", 23, "    ", None, "ship1"))
        == "1.9 (100.0, 23, ship1)"
    )


def test_iter_2_str_non_str_values_no_braces():
    assert iter_2_str([1, 2, 3], braces=False) == "1, 2, 3"
    assert iter_2_str([12, 13], braces=False) == "12, 13"
    assert (
        iter_2_str(("              \n\t    ", 1.9, 100.000, "    ", 23, "    ", None, "ship1"), braces=False)
        == "1.9, 100.0, 23, ship1"
    )


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
