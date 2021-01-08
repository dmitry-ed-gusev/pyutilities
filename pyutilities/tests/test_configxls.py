#!/usr/bin/env python
# coding=utf-8

"""
    Unit tests for ConfigurationXls class.

    Created:  Gusev Dmitrii, XX.12.2018
    Modified: Gusev Dmitrii, 06.01.2019
"""

import unittest
from pyutilities.config import ConfigurationXls, ConfigError
from pyutilities.tests.pyutils_test_helper import get_test_logger

XLS_CONFIG_FILE = 'pyutilities/tests/configs/xls_config.xlsx'
XLS_CONFIG_SHEET = 'config_sheet'


# todo: add more test cases!!!
class ConfigurationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = get_test_logger(__name__)

    def setUp(self):
        # init config before each test, don't merge with environment
        self.config = ConfigurationXls(XLS_CONFIG_FILE, XLS_CONFIG_SHEET)

    def tearDown(self):
        self.config = None

    def test_no_args(self):
        with self.assertRaises(TypeError):
            ConfigurationXls()

    def test_no_xls_file(self):
        with self.assertRaises(TypeError):
            ConfigurationXls(path_to_xls='some.xlsx')

    def test_no_xls_sheet(self):
        with self.assertRaises(TypeError):
            ConfigurationXls(config_sheet_name='some_sheet_name')

    def test_invalid_dict_to_merge(self):
        with self.assertRaises(ConfigError):
            ConfigurationXls(XLS_CONFIG_FILE, XLS_CONFIG_SHEET, dict_to_merge='sss')

    def test_simple_init(self):
        self.assertEquals(self.config.get('name2'), 'value2')
        self.assertEquals(self.config.get('name1'), 'value1')

    def test_init_dict_for_merge_is_empty_dict(self):
        config = ConfigurationXls(XLS_CONFIG_FILE, XLS_CONFIG_SHEET, dict_to_merge={})
        self.assertEquals(config.get('name2'), 'value2')
        self.assertEquals(config.get('name1'), 'value1')

    def test_init_dict_to_merge_is_nonempty_dict(self):
        config = ConfigurationXls(XLS_CONFIG_FILE, XLS_CONFIG_SHEET, dict_to_merge={'a': 'b', 'c': 'd'})
        self.assertEquals(config.get('name2'), 'value2')
        self.assertEquals(config.get('name1'), 'value1')
        self.assertEquals(config.get('a'), 'b')
        self.assertEquals(config.get('c'), 'd')

    def test_init_dict_to_merge_is_empty_list(self):
        config = ConfigurationXls(XLS_CONFIG_FILE, XLS_CONFIG_SHEET, dict_to_merge=[])
        self.assertEquals(config.get('name2'), 'value2')
        self.assertEquals(config.get('name1'), 'value1')

    def test_init_dict_to_merge_is_nonempty_list(self):
        config = ConfigurationXls(XLS_CONFIG_FILE, XLS_CONFIG_SHEET, dict_to_merge=[{'a': 'b', 'c': 'd'}, {},
                                                                                    {'aa': 'bb', 'cc': 'dd'}])
        self.assertEquals(config.get('name2'), 'value2')
        self.assertEquals(config.get('name1'), 'value1')
        self.assertEquals(config.get('a'), 'b')
        self.assertEquals(config.get('c'), 'd')
        self.assertEquals(config.get('aa'), 'bb')
        self.assertEquals(config.get('cc'), 'dd')
