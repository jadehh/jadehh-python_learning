#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_opencv_record.py.py
# @Author   : jade
# @Date     : 2021/7/16 17:03
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import cv2
from jade import GetTime
if __name__ == '__main__':
    capture = cv2.VideoCapture("data/test2.mp4")
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    save_path = "data/test3.avi".format(20)
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    video_writer = cv2.VideoWriter(save_path, fourcc, 20,
                                        (width, height))

    frame_list = []

    while True:
        ret,frame = capture.read()
        if ret is False:
            break
        frame_list.append(frame)
        # video_writer.write(frame)
        # cv2.namedWindow("result",0)
        # cv2.imshow("result",frame)
        # cv2.waitKey(1)

    frame_list.reverse()
    for frame in frame_list:
        video_writer.write(frame)
        cv2.namedWindow("result",0)
        cv2.imshow("result",frame)
        cv2.waitKey(1)
    video_writer.release()
