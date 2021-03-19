#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_windows_watch.py
# @Author   : jade
# @Date     : 2021/2/18 13:57
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     : python Windows模拟Linux Watch 操作
import os
import time
import sys
from threading import Thread
class WatchThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        index = 1
        while True:
            fp = os.popen("nvidia-smi")
            fpread = fp.read().split("\n")
            sys.stdout.write('\r' + fpread[0])
            sys.stdout.write('\r' + fpread[1])

            sys.stdout.flush()


            time.sleep(1)
            index = index + 1

if __name__ == '__main__':
    watchThread = WatchThread()