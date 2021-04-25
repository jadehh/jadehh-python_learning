#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : main.py
# @Author   : jade
# @Date     : 2021/4/25 14:48
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from ctypes import *

dll = windll.LoadLibrary("lib/test-src-shared.dll")
print(dll.test_add(1, 2))

import ctypes

lib = ctypes.CDLL('lib/test-class-shared.dll')


def opaque_ptr(name):
    cls = type(name, (ctypes.Structure,), {})
    return ctypes.POINTER(cls)


class A(object):
    _A = opaque_ptr('CPP_A')
    lib.A_new.restype = _A
    lib.A_new.argtypes = ctypes.c_char_p,
    lib.A_destruct.argtypes = _A,
    lib.A_someFunc.argtypes = _A,

    def __init__(self, name, func=lib.A_new):
        self._obj = func(name.encode('ascii'))

    def __del__(self):
        self.destruct()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.destruct()

    def destruct(self, func=lib.A_destruct):
        if self._obj:
            func(self._obj)
        self._obj = None

    def some_func(self, func=lib.A_someFunc):
        if not self._obj:
            raise RuntimeError
        func(self._obj)

with A('test') as a:
    a.some_func()

if __name__ == '__main__':
    with A('test') as a:
        a.some_func()
