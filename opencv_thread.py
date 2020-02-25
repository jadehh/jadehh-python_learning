#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : opencv_thread.py
# @Author   : jade
# @Date     : 2020/2/25 10:11
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     : opencv 线程读取视频
import cv2
import queue
import _thread
q = queue.Queue()
def captureRead(video_path):
    print(video_path)
    capture = cv2.VideoCapture(video_path)
    print(capture)
    if capture.isOpened():
        print("open success")
    else:
        print("open failed")
    while capture.isOpened():
        ret,frame = capture.read()
        q.put([ret,frame])


def captureShow():
    while True:
        if q.empty() is not True:
            capture = q.get()
            ret,frame = capture[0],capture[1]
            if ret:
                cv2.namedWindow("windows",0)
                cv2.imshow("result",frame)
                cv2.waitKey(1)

if __name__ == '__main__':
    # 创建两个线程
    video_path = "rtsp://admin:samples123@192.168.35.119/Streaming/Channels/1"
    captureRead(video_path)
    _thread.start_new_thread(captureRead, ("rtsp://admin:samples123@192.168.35.119/Streaming/Channels/1",))
    _thread.start_new_thread(captureShow, ())
