#!/usr/bin/env python
# coding=utf-8

"""

    Unit tests for pylog module.

    Created:  Dmitrii Gusev, 15.04.2019
    Modified:
"""

import unittest
from logging import Logger, NullHandler
from pyutilities.pylog import init_logger, setup_logging
from pyutilities.pyexception import PyUtilsException
from pyutilities.tests.pyutils_test_helper import get_test_logger


class PylogTest(unittest.TestCase):

    def setUp(self):
        self.log.debug('setUp() is working.')

    def tearDown(self):
        self.log.debug('tearDown() is working.')

    @classmethod
    def setUpClass(cls):
        cls.log = get_test_logger(__name__)
        cls.log.debug('setUpClass() is working.')

    @classmethod
    def tearDownClass(cls):
        cls.log.debug('tearDownClass() is working.')

    def test_init_logger_empty_name(self):
        with self.assertRaises(PyUtilsException):
            init_logger(None)

    def test_init_logger_return_logger(self):
        log = init_logger('some_name1')
        self.assertTrue(isinstance(log, Logger))

    def test_init_logger_add_null_handler(self):
        log = init_logger('some_name2')
        self.assertTrue(NullHandler in log.handlers)

    def test_init_logger_doesnt_add_null_handler(self):
        log = init_logger('some_name3', add_null_handler=False)
        self.assertTrue(NullHandler not in log.handlers)
