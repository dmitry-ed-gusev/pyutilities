#!/usr/bin/env python
# coding=utf-8

"""
    Unit tests for ConfigurationXls class.

    Created:  Gusev Dmitrii, XX.12.2018
    Modified: Gusev Dmitrii, 10.01.2021
"""

import unittest
from pyutilities.config import ConfigurationXls, ConfigError
from pyutilities.tests.pyutils_test_helper import get_test_logger

XLSX_CONFIG_FILE = 'pyutilities/tests/configs/xlsx_config.xlsx'  # xlsx format (Excel 2010)
XLS_CONFIG_FILE = 'pyutilities/tests/configs/xls_config.xls'     # xls format (old Excel)
CONFIG_SHEET = 'config_sheet'


# todo: add more test cases!!!
class ConfigurationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = get_test_logger(__name__)

    def setUp(self):
        # init config before each test, don't merge with environment
        self.config_xls = ConfigurationXls(XLS_CONFIG_FILE, CONFIG_SHEET)
        self.config_xlsx = ConfigurationXls(XLSX_CONFIG_FILE, CONFIG_SHEET)

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
            ConfigurationXls(XLS_CONFIG_FILE, CONFIG_SHEET, dict_to_merge='sss')

    def test_simple_xls_init(self):
        self.assertEquals(self.config_xls.get('name2xls'), 'value2')
        self.assertEquals(self.config_xls.get('name1xls'), 'value1')

    def test_simple_xlsx_init(self):
        self.assertEquals(self.config_xlsx.get('name2xlsx'), 'value2')
        self.assertEquals(self.config_xlsx.get('name1xlsx'), 'value1')

    def test_init_dict_for_merge_is_empty_dict_xls(self):
        config_xls = ConfigurationXls(XLS_CONFIG_FILE, CONFIG_SHEET, dict_to_merge={})
        self.assertEquals(config_xls.get('name2xls'), 'value2')
        self.assertEquals(config_xls.get('name1xls'), 'value1')

    def test_init_dict_for_merge_is_empty_dict_xlsx(self):
        config_xls = ConfigurationXls(XLSX_CONFIG_FILE, CONFIG_SHEET, dict_to_merge={})
        self.assertEquals(config_xls.get('name2xlsx'), 'value2')
        self.assertEquals(config_xls.get('name1xlsx'), 'value1')

    def test_init_dict_to_merge_is_nonempty_dict_xls(self):
        config_xls = ConfigurationXls(XLS_CONFIG_FILE, CONFIG_SHEET, dict_to_merge={'a': 'b', 'c': 'd'})
        self.assertEquals(config_xls.get('name2xls'), 'value2')
        self.assertEquals(config_xls.get('name1xls'), 'value1')
        self.assertEquals(config_xls.get('a'), 'b')
        self.assertEquals(config_xls.get('c'), 'd')

    def test_init_dict_to_merge_is_nonempty_dict_xlsx(self):
        config_xls = ConfigurationXls(XLSX_CONFIG_FILE, CONFIG_SHEET, dict_to_merge={'a': 'b', 'c': 'd'})
        self.assertEquals(config_xls.get('name2xlsx'), 'value2')
        self.assertEquals(config_xls.get('name1xlsx'), 'value1')
        self.assertEquals(config_xls.get('a'), 'b')
        self.assertEquals(config_xls.get('c'), 'd')

    def test_init_dict_to_merge_is_empty_list_xls(self):
        config_xls = ConfigurationXls(XLS_CONFIG_FILE, CONFIG_SHEET, dict_to_merge=[])
        self.assertEquals(config_xls.get('name2xls'), 'value2')
        self.assertEquals(config_xls.get('name1xls'), 'value1')

    def test_init_dict_to_merge_is_empty_list_xlsx(self):
        config_xls = ConfigurationXls(XLSX_CONFIG_FILE, CONFIG_SHEET, dict_to_merge=[])
        self.assertEquals(config_xls.get('name2xlsx'), 'value2')
        self.assertEquals(config_xls.get('name1xlsx'), 'value1')

    def test_init_dict_to_merge_is_nonempty_list_xls(self):
        config_xls = ConfigurationXls(XLS_CONFIG_FILE, CONFIG_SHEET, dict_to_merge=[{'a': 'b', 'c': 'd'}, {},
                                                                                    {'aa': 'bb', 'cc': 'dd'}])
        self.assertEquals(config_xls.get('name2xls'), 'value2')
        self.assertEquals(config_xls.get('name1xls'), 'value1')
        self.assertEquals(config_xls.get('a'), 'b')
        self.assertEquals(config_xls.get('c'), 'd')
        self.assertEquals(config_xls.get('aa'), 'bb')
        self.assertEquals(config_xls.get('cc'), 'dd')

    def test_init_dict_to_merge_is_nonempty_list_xlsx(self):
        config_xls = ConfigurationXls(XLSX_CONFIG_FILE, CONFIG_SHEET, dict_to_merge=[{'a': 'b', 'c': 'd'}, {},
                                                                                    {'aa': 'bb', 'cc': 'dd'}])
        self.assertEquals(config_xls.get('name2xlsx'), 'value2')
        self.assertEquals(config_xls.get('name1xlsx'), 'value1')
        self.assertEquals(config_xls.get('a'), 'b')
        self.assertEquals(config_xls.get('c'), 'd')
        self.assertEquals(config_xls.get('aa'), 'bb')
        self.assertEquals(config_xls.get('cc'), 'dd')
