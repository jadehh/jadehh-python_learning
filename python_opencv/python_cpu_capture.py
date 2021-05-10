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
    video_path = "/home/jade/sda2/Data/TaiCang/Container/2020-09-04/front/2020-09-04-07-27-29.mp4"
    capture = cv2.VideoCapture(video_path)
    index = 0
    cv2.namedWindow("cpu",0)
    while True:
        ret,frame = capture.read()
        if ret is False:
            break
        frame = cv2.resize(frame,(416,416))
        cv2.imwrite("result.jpg",frame)

        cv2.imshow("cpu",frame)
        cv2.waitKey(0)
        index = index + 1
        if index %100==0:
            print("正在播放视频,index = {},image cols = {}".format(index,frame.shape[1]))
