#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_video_to_image.py
# @Author   : jade
# @Date     : 2021/9/13 11:17
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import cv2
import os
from jade import GetLastDir,CreateSavePath
from jade import GetTime
from jade import ProgressBar
def VideoToImage(video_path):
    capture = cv2.VideoCapture(video_path)
    save_path = CreateSavePath(GetLastDir(video_path))
    image_list = []
    progressBar = ProgressBar(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    while True:
        ret,frame = capture.read()
        if ret is False:
            break
        image_path = os.path.join(save_path,GetTime()+".jpg")
        image_list.append(image_path)
        cv2.imencode('.jpg', frame)[1].tofile(image_path)
        progressBar.update()



if __name__ == '__main__':
    VideoToImage(r"C:\Users\Administrator\Desktop\15e37b9efa78ef59629d6d4edb4477b7.mp4")