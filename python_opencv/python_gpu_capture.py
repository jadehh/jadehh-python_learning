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
    gpu_capture:cv2.cudacodec_VideoReader = cv2.cudacodec.createVideoReader("rtsp://admin:samples123@192.168.35.211:554/h264/ch1/main/av_stream")
    if gpu_capture.nextFrame()[0]:
        print("打开成功")
    else:
        print("打开失败")
    index = 0
    while True:
        ret,frame = gpu_capture.nextFrame()
        frame = frame.download()
        if ret is False:
            break
        index = index + 1
        if index %100==0:
            print("正在播放视频,index = {},image cols = {}".format(index,frame.shape[1]))
