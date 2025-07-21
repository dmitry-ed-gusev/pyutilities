#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for io_utilities module.

    Created:  Dmitrii Gusev, 12.10.2022
    Modified: Dmitrii Gusev, 18.07.2025
"""

import pytest
from mock import mock_open, patch

from pyutilities.io.io_utils import _list_files, list_files, read_yaml

MOCK_OPEN_METHOD = "pyutilities.io.io_utils.open"
MOCK_WALK_METHOD = "pyutilities.io.io_utils.walk"


def test_parse_yaml_ioerror():
    with pytest.raises(IOError):
        with patch(MOCK_OPEN_METHOD, mock_open(read_data="name:\tvalue"), create=True):
            read_yaml("foo_ioerror.file")


def test_parse_yaml_empty_paths():
    for path in ["", "   "]:
        with pytest.raises(IOError):
            with patch(MOCK_OPEN_METHOD, mock_open(read_data="n: v"), create=True):
                read_yaml(path)


def test_aaa():
    pass


def test_bbb():
    pass


def test_file2str():
    pass


def test_read_yaml():
    # def test_parse_yaml():
    # with patch(MOCK_OPEN_METHOD, mock_open(read_data="name123: value123"), create=True):
    #     result = read_yaml("foo_ok.file")
    #     assert result["name123"] == "value123"
    pass


def test_read_yaml_ioerror():
    with pytest.raises(IOError):
        with patch(MOCK_OPEN_METHOD, mock_open(read_data="name:\tvalue"), create=True):
            read_yaml("foo_ioerror.file")


def test_read_yaml_empty_paths():
    for path in ["", "   "]:
        with pytest.raises(IOError):
            with patch(MOCK_OPEN_METHOD, mock_open(read_data="n: v"), create=True):
                read_yaml(path)


def test_compress_file():
    pass


# class IOUtilsTest(unittest.TestCase):

#     def test_list_files_invalid_paths(self):
#         for path in [
#             "",
#             "    ",
#             "not-existing-path",
#             "__init__.py",
#         ]:  # the last one - existing python file
#             with self.assertRaises(IOError):
#                 list_files(path)

#     @patch(MOCK_WALK_METHOD)
#     def test_internal_list_files(self, mock_walk):
#         mock_walk.return_value = [("/path", ["dir1"], ["file1"])]

#         files = []
#         _list_files("zzz", files, True)
#         self.assertEqual(1, len(files))
#         self.assertEqual("/path/file1", files[0])
