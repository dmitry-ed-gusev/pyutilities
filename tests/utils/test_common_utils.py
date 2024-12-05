#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Unit tests for utils module from [pyutilities] library. Covers most of methods in a module.

    Created:  Gusev Dmitrii, 2017
    Modified: Gusev Dmitrii, 22.11.2022
"""

from itertools import count

from pyutilities.utils.common_utils import singleton


def test_singleton():

    @singleton
    class Obj(object):
        _ids = count(0)

        def __init__(self):
            self.id = next(self._ids)

        def get_id(self):
            return self.id

    instance1 = Obj()
    instance2 = Obj()

    assert instance1 == instance2
    assert instance1.id == instance2.id
