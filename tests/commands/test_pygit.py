#!/usr/bin/env python
# coding=utf-8

"""
    Unit tests for pygit module/PyGit class.

    Created:  Dmitrii Gusev, 24.04.2019
    Modified: Dmitrii Gusev, 12.10.2022
"""

import unittest
from pyutilities.commands.pygit import PyGit


class PyGitTest(unittest.TestCase):

    def setUp(self):
        self.pygit = PyGit("http://stash.server.com/scm")

    def tearDown(self):
        # method just for the demo purpose
        pass

    @classmethod
    def setUpClass(cls):
        # method just for the demo purpose
        pass

    @classmethod
    def tearDownClass(cls):
        # method just for the demo purpose
        pass

    def test(self):
        # todo: implement tests!
        pass
