# -*- coding: utf-8 -*-

from itertools import count

from pyutilities.utils.decorators import singleton_v1, singleton_v2,  debug_benchmark
from pyutilities.utils.decorators import threadsafe_function, debug_function_name


def test_singleton_v1():

    @singleton_v1
    class Obj(object):
        _ids = count(0)

        def __init__(self):
            self.id = next(self._ids)

        def get_id(self):
            return self.id

    instance1 = Obj()
    instance2 = Obj()

    assert instance1 == instance2
    assert instance1 is instance2
    assert instance1.id == instance2.id
    assert instance1.id == 0
    assert instance2.id == 0


def test_singleton_v2():

    @singleton_v2
    class Obj(object):
        _ids = count(0)

        def __init__(self):
            self.id = next(self._ids)

        def get_id(self):
            return self.id

    instance1 = Obj()
    instance2 = Obj()

    assert instance1 == instance2
    assert instance1 is instance2
    assert instance1.id == instance2.id
    assert instance1.id == 0
    assert instance2.id == 0


def test_threadsafe_function():
    # TODO: implement test!
    pass


def test_debug_benchmark():

    @debug_benchmark
    def func_sleep():
        import time
        time.sleep(3)

    func_sleep()


def test_debug_function_name():
    # TODO: implement test!
    pass
