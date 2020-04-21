#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_manage_thread.py
# @Author   : jade
# @Date     : 2020/2/25 10:09
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     : python线程管理
#!/usr/bin/python3

import _thread
import time

# 为线程定义一个函数
def print_time(threadName, delay):
   count = 0
   while True:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

if __name__ == '__main__':
    print("Error: 无法启动线程")