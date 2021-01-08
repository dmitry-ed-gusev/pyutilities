#!/usr/bin/env python
# coding=utf-8

"""
    Unit tests for Configuration class.

    Created:  Gusev Dmitrii, XX.08.2017
    Modified: Gusev Dmitrii, 04.03.2019
"""

import os
import unittest
from mock import patch
from pyutilities.config import Configuration, ConfigError
from pyutilities.tests.pyutils_test_helper import get_test_logger

CONFIG_PATH = 'pyutilities/tests/configs'
CONFIG_MODULE_MOCK_YAML = 'pyutilities.config.parse_yaml'
CONFIG_MODULE_MOCK_OS = 'pyutilities.config.os'


class ConfigurationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = get_test_logger(__name__)

    def setUp(self):
        # init config instance before each test, don't merge with environment
        self.config = Configuration(is_merge_env=False)

    def tearDown(self):
        # dereference config instance after each test
        self.config = None

    def test_load_invalid_path(self):
        for invalid_path in ['', "", '   ', "    ", "non-exist path"]:
            with self.assertRaises(ConfigError):
                self.config.load(invalid_path)

    def test_merge_config_files(self):
        self.config.load(CONFIG_PATH)  # <- load all yaml configs from specified location
        self.assertEqual(self.config.get("section1.key1"), "value1")
        self.assertEqual(self.config.get("section2.key3"), "value3")

    def test_merge_env_variables(self):
        os.environ["simple_key"] = "env_value"
        self.config.load(CONFIG_PATH, is_merge_env=False)
        self.assertEqual(self.config.get("simple_key"), "file_value")
        self.config.merge_env()
        self.assertEqual(self.config.get("simple_key"), "env_value")

    # todo: add more test cases here
    def test_merge_dict_single_on_init(self):
        dict_to_merge = {'a': 'b', 'c': 'd', 'aa.bb': 'eee'}
        config = Configuration(path_to_config=CONFIG_PATH, dict_to_merge=dict_to_merge,
                               is_merge_env=True)
        self.assertEquals(config.get("section1.key1"), "value1")
        self.assertEquals(config.get("section2.key3"), "value3")
        self.assertEquals(config.get('a'), 'b')
        self.assertEquals(config.get('c'), 'd')
        self.assertEquals(config.get('aa.bb'), 'eee')

    # todo: add more test cases here
    def test_merge_dict_list_on_init(self):
        dict_list_to_merge = [{'a': 'b'}, {'c': 'd'}, {'aa.bb': 'eee'}]
        config = Configuration(path_to_config=CONFIG_PATH, dict_to_merge=dict_list_to_merge,
                               is_merge_env=True)
        self.assertEquals(config.get("section1.key1"), "value1")
        self.assertEquals(config.get("section2.key3"), "value3")
        self.assertEquals(config.get('a'), 'b')
        self.assertEquals(config.get('c'), 'd')
        self.assertEquals(config.get('aa.bb'), 'eee')

    # todo: implement test case
    def test_append_dict(self):
        pass

    def test_get_not_existing_property(self):
        with self.assertRaises(ConfigError):
            self.config.get("non_existing")

    def test_get_not_exisitng_complex_property(self):
        self.config.set('level1', None)
        with self.assertRaises(ConfigError):
            self.config.get('level1.level2')

    def test_get_top_property(self):
        self.config.merge_dict({'f': 'h'})
        self.assertEqual(self.config.get('f'), 'h')

    def test_set_top_property(self):
        self.config.set('m', 'n')
        self.assertEqual(self.config.get('m'), 'n')

    def test_get_deep_property(self):
        self.config.merge_dict({'x': {'y': {'z': '100'}}})
        self.assertEqual(self.config.get('x.y.z'), '100')

    def test_set_deep_property(self):
        self.config.set('a.b.c', 'e')
        self.assertEqual(self.config.get('a.b.c'), 'e')

    def test_replace_deep_property(self):
        self.config.merge_dict({'a': {'b': {'c': 'd'}}})
        self.assertEqual(self.config.get('a.b.c'), 'd')
        self.config.set('a.b.c', 'e')
        self.assertEqual(self.config.get('a.b.c'), 'e')

    @patch(CONFIG_MODULE_MOCK_YAML)
    @patch(CONFIG_MODULE_MOCK_OS)
    def test_load_from_single_yaml(self, mock_os, mock_parse_yaml):
        # set returned results for mocks
        mock_os.exists.return_value = True
        mock_os.isfile.return_value = True
        mock_os.isdir.return_value = False
        mock_parse_yaml.return_value = {"key": "value"}

        # check that key doesn't exist in config
        with self.assertRaises(ConfigError):
            self.config.get("key")

        # load config from mocked file
        self.config.load("/config/myyaml123.yml", False)
        # check that now key exists in config
        self.assertEqual(self.config.get("key"), "value")

    @patch(CONFIG_MODULE_MOCK_YAML)
    @patch(CONFIG_MODULE_MOCK_OS)
    def test_load_from_directory(self, mock_os, mock_parse_yaml):
        # mock for os.path()
        mock_os.exists.return_value = True
        mock_os.isfile.return_value = True
        mock_os.isdir.return_value = True
        # mock for os.listdir() - list of files
        mock_os.listdir.return_value = ['file1.yml', 'file2.yml']
        # each call to parse_yaml() will return next value
        mock_parse_yaml.side_effect = [{"key1": "value1"}, {"key2": "value2"}]

        self.config.load("mydir", False)  # load config
        # assertions
        self.assertEqual(self.config.get("key1"), "value1")
        self.assertEqual(self.config.get("key2"), "value2")

    @patch.object(Configuration, 'load')
    def test_init_with_path(self, mock_load):
        # case 1 - merge with environment
        Configuration('some_path1', is_merge_env=True)
        mock_load.assert_called_with('some_path1', True)
        # case 2 - don't merge with environment
        Configuration('some_path2', is_merge_env=False)
        mock_load.assert_called_with('some_path2', False)

    def test_init_with_dict_override(self):
        config = Configuration(dict_to_merge={'key': 'value'}, is_override_config=True)
        self.assertEqual(config.get('key'), 'value')

    @patch(CONFIG_MODULE_MOCK_YAML)
    @patch(CONFIG_MODULE_MOCK_OS)  # name for patch should be equals to import in real module!
    def test_init_with_dict_dont_override(self, mock_os, mock_parse_yaml):
        # set returned results for mocks
        mock_os.exists.return_value = True
        mock_os.isfile.return_value = True
        mock_os.isdir.return_value = False
        mock_parse_yaml.return_value = {"key": "initial_value"}
        # init config instance
        config = Configuration(path_to_config='yaml_file.yml',
                               dict_to_merge={'key': 'new_value', 'aaa': 'bbb'}, is_override_config=False)
        # assertions
        self.assertEqual(config.get('key'), 'initial_value')

    # todo: possible wrong behaviour: can't get multi-level key (a.b.c) after merge_dict()
    def test_merge_dict_multi_level_key_issue(self):
        new_dict = {'name.subname3': 'subvalue3'}

        self.config.set('name', {'subname1': 'subvalue1', 'subname2': 'subvalue2'})
        self.config.merge_dict(new_dict)

        # line that generates issue
        with self.assertRaises(ConfigError):
            print(self.config.get('name.subname3'))
