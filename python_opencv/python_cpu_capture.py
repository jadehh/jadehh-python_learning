#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_cpu_capture.py
# @Author   : jade
# @Date     : 2021/4/27 19:05
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import cv2
if __name__ == '__main__':
    #video_path = "rtsp://admin:samples123@192.168.35.211:554/h264/ch1/main/av_stream"
    video_path = "rtmp://192.168.40.202/live/container_ocr"
    capture = cv2.VideoCapture(video_path)
    index = 0
    cv2.namedWindow("cpu",0)
    while True:
        ret,frame = capture.read()
        if ret is False:
            break
        cv2.imwrite("result.jpg",frame)
        cv2.imshow("cpu",frame)
        cv2.waitKey(1)


