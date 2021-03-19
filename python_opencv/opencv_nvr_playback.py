#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : opencv_nvr_playback.py
# @Author   : jade
# @Date     : 2021/3/19 9:53
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import cv2

if __name__ == '__main__':
    video_path = "rtsp://admin:samples123@192.168.35.99:554/Streaming/tracks/101?starttime=20210316t000000z&endtime=20210317t000000z"
    capture = cv2.VideoCapture(video_path)
    while True:
        ret,frame = capture.read()
        cv2.namedWindow("result",0)
        cv2.imshow("result",frame)
        cv2.waitKey(0)