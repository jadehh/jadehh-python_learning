#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_manage_process.py
# @Author  : jade
# @Date    : 20-3-19 上午9:19
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    : Python线程管理

from multiprocessing import Process,Queue
import time
'''
如果While循环中什么都不做,CPU单线程资源将会占满100%
加入time.sleep(0.01), CPU单线程资源将会少了很多
'''
class PythonProcess(Process):
    def __init__(self):
        super().__init__()
        Process.__init__(self)
    def run(self):
        while True:
            time.sleep(0.01)
            pass



'''
进程中循环接受队列中的值,单进程CPU占用单线程130%
加time.sleep(0.01),变成0.7,接受进程会收到添加进程的影响
'''
class PythonQueueProcess(Process):
    def __init__(self,processqueue:Queue):
        super().__init__()
        self.processqueue = processqueue
        Process.__init__(self)

    def run(self):
        while True:
            tmp = self.processqueue.get()


class PythonAddQueueProcess(Process):
    def __init__(self,processqueue:Queue):
        super().__init__()
        self.processqueue = processqueue
        Process.__init__(self)

    def run(self):
        while True:
            self.processqueue.put(1)
            time.sleep(0.01)


if __name__ == '__main__':
    processqueues = [Queue(maxsize=10)  for _ in ["1"] * 4]
    for i in range(2):
        python_add_process = PythonAddQueueProcess(processqueues[i])
        python_add_process.start()
        print("add process pid = {}".format(python_add_process.pid))
        python_process = PythonQueueProcess(processqueues[i])
        python_process.start()
        print("process queue pid = {}".format(python_process.pid))