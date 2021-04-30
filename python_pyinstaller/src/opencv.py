#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_cpu_capture.py
# @Author   : jade
# @Date     : 2021/4/27 19:05
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import sys
sys.path.append("../lib")
import cv2
from config import  video_path
def showWindow():
    #video_path = "rtsp://admin:samples123@192.168.35.211:554/h264/ch1/main/av_stream"
    video_path = "/home/jade/sda2/Data/TaiCang/Container/2020-09-04/front/2020-09-04-07-27-29.mp4"
    gpu_capture:cv2.cudacodec_VideoReader = cv2.cudacodec.createVideoReader(video_path)
    if gpu_capture.nextFrame()[0]:
        print("打开成功")
    else:
        print("打开失败")
    index = 0
    cv2.namedWindow("gpu",0)
    while True:
        ret,frame = gpu_capture.nextFrame() ## BRGA格式
        frame = frame.download()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)

        cv2.imshow("gpu",frame)
        cv2.waitKey(1)
        if ret is False:
            break
        index = index + 1
        if index %100==0:
            print("正在播放视频,index = {},image cols = {}".format(index,frame.shape[1]))
if __name__ == '__main__':
    showWindow()

