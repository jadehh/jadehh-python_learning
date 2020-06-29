#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_stop_thread.py
# @Author  : jade
# @Date    : 20-5-22 下午1:13
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
##
import psutil
import os
import signal
def getPidNumberofProcessName(processname):
    pidnumbers = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if processname == pinfo["name"]:
                pidnumbers.append(pinfo["pid"])
    return pidnumbers

if __name__ == '__main__':
    pidnumbers = (getPidNumberofProcessName("python"))
    for pidnumber in pidnumbers:
        if pidnumber != os.getpid():
            try:
                a = os.kill(pidnumber, signal.SIGKILL)
                # a = os.kill(pid, signal.9) #　与上等效
                print('已杀死pid为%s的进程,　返回值是:%s' % (pidnumber, a))
            except Exception as  e:
                print(e)



