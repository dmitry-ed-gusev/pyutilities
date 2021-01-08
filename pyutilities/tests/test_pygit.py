#!/usr/bin/env python
# coding=utf-8

"""

    Unit tests for pygit module/PyGit class.

    Created:  Dmitrii Gusev, 24.04.2019
    Modified: Dmitrii Gusev, 25.05.2019

"""

import unittest
from pyutilities.tests.pyutils_test_helper import get_test_logger
from pyutilities.pygit import PyGit


class PyGitTest(unittest.TestCase):

    def setUp(self):
        self.log.debug('setUp() is working.')
        self.pygit = PyGit('http://stash.server.com/scm')

    def tearDown(self):
        self.log.debug('tearDown() is working.')

    @classmethod
    def setUpClass(cls):
        cls.log = get_test_logger(__name__)
        cls.log.debug('setUpClass() is working.')

    @classmethod
    def tearDownClass(cls):
        cls.log.debug('tearDownClass() is working.')

    def test(self):
        pass
