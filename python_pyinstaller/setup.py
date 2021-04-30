#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : setup.py
# @Author   : jade
# @Date     : 2021/4/30 11:13
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from distutils.core import setup
from Cython.Build import cythonize
import os
file_list = os.listdir("src")
modules = []
for file in file_list:
    if file.split(".")[-1] == "py":
        modules.append("src/" + file)

import shutil

if os.path.exists("src_copy"):
    shutil.rmtree("src_copy")
    os.mkdir("src_copy")

else:
    os.mkdir("src_copy")

copy_modudles = []
for file in modules:
    copy_modudles.append("src_copy/" + file.split("/")[-1][:-3] + ".pyx")
    shutil.copy(file, "src_copy/" + file.split("/")[-1][:-3] + ".pyx")

setup(
    ext_modules=cythonize(copy_modudles)
)

if __name__ == '__main__':
    setup()
