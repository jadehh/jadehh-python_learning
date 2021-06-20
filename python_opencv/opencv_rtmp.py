#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : opencv_rtmp.py
# @Author   : jade
# @Date     : 2021/6/17 16:27
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import cv2
if __name__ == '__main__':
    capture = cv2.VideoCapture("rtmp://192.168.35.120/live/test2")
    while True:
        ret,frame = capture.read()
        print(frame.shape)