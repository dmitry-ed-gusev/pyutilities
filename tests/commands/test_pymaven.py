#!/usr/bin/env python
# coding=utf-8

"""
    Unit tests for pygit module/PyMaven class.

    Created:  Dmitrii Gusev, 28.05.2019
    Modified: Dmitrii Gusev, 12.10.2022
"""

import os
import unittest
from pyutilities.commands.pymaven import PyMaven

MVN_SPECIAL_SETTINGS = "mvn_settings_empty.xml"
MVN_SPECIAL_SETTINGS_NON_EXISTING = "non-existing-mvn-settings.xml"
MVN_DEFAULT_CMD = cmd = ["mvn", "clean", "install"]


class PyMavenTest(unittest.TestCase):

    def setUp(self):
        self.pymaven = PyMaven()
        self.pymaven_with_settings = PyMaven(MVN_SPECIAL_SETTINGS)

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

    def test_pymaven_raise_exception_on_non_exitent_settings(self):
        with self.assertRaises(FileNotFoundError):
            self.pymaven_with_non_existing_settings = PyMaven(MVN_SPECIAL_SETTINGS_NON_EXISTING)

    def test_append_mvn_settings_empty_settings(self):
        expected = ["mvn", "clean", "install"]
        # test itself
        self.assertListEqual(expected, self.pymaven.append_mvn_settings(MVN_DEFAULT_CMD))

    def test_append_mvn_settings_non_empty_settings(self):
        expected = ["mvn", "clean", "install", "-s", os.path.abspath(MVN_SPECIAL_SETTINGS)]
        # test itself
        self.assertListEqual(expected, self.pymaven_with_settings.append_mvn_settings(MVN_DEFAULT_CMD))
