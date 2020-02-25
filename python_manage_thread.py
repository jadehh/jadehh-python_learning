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
    # 创建两个线程
    try:
        _thread.start_new_thread(print_time, ("Thread-1", 2,))
        _thread.start_new_thread(print_time, ("Thread-2", 4,))
    except:
        print("Error: 无法启动线程")

    while 1:
        pass


