#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_chinese_to_py.py
# @Author   : jade
# @Date     : 2021/7/22 10:32
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from xpinyin import Pinyin

# 实例拼音转换对象
p = Pinyin()
# 进行拼音转换
ret = p.get_pinyin(u"汉语拼音转换", tone_marks='marks')
ret1 = p.get_pinyin(u"汉语拼音转换", tone_marks='numbers')
print(ret + '\n' + ret1)
