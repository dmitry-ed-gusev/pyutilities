#!/usr/bin/env python
# coding=utf-8

"""

    Unit tests for fedit utility.

    Created:  Gusev Dmitrii, 26.09.2018
    Modified: Dmitrii Gusev, 10.01.2021

"""

import unittest
from pyutilities.tests.pyutils_test_helper import get_test_logger


# todo: implement unit tests for fedit utility
class FEditTest(unittest.TestCase):

    def setUp(self):
        print("FEditTest.setUp()")

    def tearDown(self):
        print("FEditTest.tearDown()")

    @classmethod
    def setUpClass(cls):
        cls.log = get_test_logger(__name__)
        cls.log.debug('setUpClass() is working.')

    @classmethod
    def tearDownClass(cls):
        cls.log.debug('tearDownClass() is working.')

    def test(self):
        # todo: implement unit test
        pass
