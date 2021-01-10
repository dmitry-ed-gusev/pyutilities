#!/usr/bin/env python
# coding=utf-8

"""

    Unit tests for utils module from [pyutilities] library. Covers most of methods in a module.

    Created:  Gusev Dmitrii, 2017
    Modified: Gusev Dmitrii, 26.09.2018

"""

import unittest
from mock import patch, mock_open
from pyutilities.utils import parse_yaml, filter_str, list_files, _list_files
from pyutilities.tests.pyutils_test_helper import get_test_logger


MOCK_OPEN_METHOD = 'pyutilities.utils.open'
MOCK_WALK_METHOD = 'pyutilities.utils.walk'


class ConfigurationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = get_test_logger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_parse_yaml(self):
        with patch(MOCK_OPEN_METHOD, mock_open(read_data='name: value'), create=True):
            result = parse_yaml('foo_ok.file')
        self.assertEquals('value', result['name'])

    def test_parse_yaml_ioerror(self):
        with self.assertRaises(IOError):
            with patch(MOCK_OPEN_METHOD, mock_open(read_data='name:\tvalue'), create=True):
                parse_yaml('foo_ioerror.file')

    def test_parse_yaml_empty_paths(self):
        for path in ['', '   ']:
            with self.assertRaises(IOError):
                with patch(MOCK_OPEN_METHOD, mock_open(read_data='n: v'), create=True):
                    parse_yaml(path)

    def test_list_files_invalid_paths(self):
        for path in ['', '    ', 'not-existing-path', '__init__.py']:  # the last one - existing python file
            with self.assertRaises(IOError):
                list_files(path)

    @patch(MOCK_WALK_METHOD)
    def test_internal_list_files(self, mock_walk):
        mock_walk.return_value = [('/path', ['dir1'], ['file1'])]

        files = []
        _list_files('zzz', files, True)
        self.assertEquals(1, len(files))
        self.assertEquals('/path/file1', files[0])

    def test_filter_str_for_empty(self):
        for string in ['', '    ', None]:
            self.assertEquals(string, filter_str(string))

    def test_filter_str_for_string(self):
        self.assertEquals('45, .555', filter_str('+45, *@.555'))
        self.assertEquals('улица  Правды. 11,', filter_str('улица + =Правды. 11,'))
        self.assertEquals('3-5-7', filter_str('3-5-7'))
        self.assertEquals('zzzz. , fgh ', filter_str('zzzz. ??, fgh *'))
