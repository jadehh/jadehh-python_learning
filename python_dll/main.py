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

print(dll)
