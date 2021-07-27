#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_pynotify_demo.py
# @Author   : jade
# @Date     : 2021/7/14 12:16
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
# -*- coding: utf-8 -*-
# !/usr/bin/env python
import os
import datetime
import pyinotify
import logging
from jade import GetTimeStamp,Thread
import time


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        PATH = os.path.join("demo.txt")
        self.file = open(PATH)
        self.position = 0
        self.print_lines()

    def process_IN_MODIFY(self, event):
        print ('event received')
        self.print_lines()

    def print_lines(self):
        new_lines = self.file.read()
        last_n = new_lines.rfind('\n')
        if last_n >= 0:
            self.position += last_n + 1
            print (new_lines[:last_n])
        else:
            print ('no line')
        self.file.seek(self.position)



class WriteTxt(Thread):
    def __init__(self):
        super(WriteTxt, self).__init__()
    def run(self):
        while True:
            with open("demo.txt","a") as f:
                f.write(GetTimeStamp()+"\n")
            time.sleep(1)
if __name__ == '__main__':
    writeTxt = WriteTxt()
    writeTxt.start()
    wm = pyinotify.WatchManager()
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch("demo.txt", pyinotify.IN_MODIFY, rec=True)
    notifier.loop()
