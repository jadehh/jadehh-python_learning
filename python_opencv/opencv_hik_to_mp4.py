#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : opencv_hik_to_mp4.py
# @Author   : jade
# @Date     : 2021/5/31 15:06
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_opencv_record_video.py
# @Author  : jade
# @Date    : 20-4-27 下午3:58
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
from threading import Thread
from queue import Queue
from jade import *
import argparse


class read_video(Thread):
    def __init__(self, video_path, framequeue):
        self.video_path = video_path
        self.framequeue = framequeue
        Thread.__init__(self)

    def run(self):
        print(self.video_path)
        capture = cv2.VideoCapture(self.video_path)

        if capture.isOpened():
            print("read success")
        else:
            print("read failure")
        while capture.isOpened():
            ret, frame = capture.read()
            if ret:
                self.framequeue.put((ret,frame))
            else:
                self.framequeue.put((ret,frame))
                break


class record_video(Thread):
    def __init__(self, framequeue, path):
        self.framequeue = framequeue
        self.save_path =GetPreviousDir(path) + "/" + GetLastDir(path).split(".")[0] + ".avi"
        self.fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

        Thread.__init__(self)

    def run(self):
        ret,frame = self.framequeue.get()
        self.videoWriter = cv2.VideoWriter(self.save_path,self.fourcc, 30, (frame.shape[1], frame.shape[0]))
        while True:
            ret, frame = self.framequeue.get()
            if ret:
                self.videoWriter.write(frame)
                print("正在存储视频 shape = {} ".format(frame.shape))
            else:
                break


def start_record(args):
    framequeue = Queue(100)
    read_video_process = read_video(args.path,
                                        framequeue)
    read_video_process.start()
    record_video_process = record_video(framequeue,args.path)
    record_video_process.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, help='please select video path')
    args = parser.parse_args()
    print(args.path)
    start_record(args)
