#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_torch_process.py
# @Author   : jade
# @Date     : 2021/6/3 18:15
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from python_process.SuperPointNet import SuperPointFrontend
import multiprocessing
import time
class TestProcess(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)

    def run(self):
        model = SuperPointFrontend(
            "models/keypoint_det/models.pth")
        while True:
            time.sleep(1)


if __name__ == '__main__':
    num_processes = 2
    for i in range(num_processes):
        testProcess = TestProcess()
        testProcess.start()

