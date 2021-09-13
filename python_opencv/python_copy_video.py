#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_copy_video.py
# @Author   : jade
# @Date     : 2021/8/11 14:50
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import cv2
import os
import shutil
from jade import GetTime,CreateSavePath
def VideoToImage(video_path):
    capture = cv2.VideoCapture(video_path)
    save_path = CreateSavePath("tmp/video/")
    image_list = []
    while True:
        ret,frame = capture.read()
        if ret is False:
            break
        image_path = os.path.join(save_path,GetTime()+".jpg")
        image_list.append(image_path)
        cv2.imencode('.jpg', frame)[1].tofile(image_path)
    return image_list


def ImageToVideo(video_path,image_list,save_video_path):
    capture = cv2.VideoCapture(video_path)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc =  cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    video_writer = cv2.VideoWriter(save_video_path, fourcc, 20,
                                        (width, height))
    while True:
        ret,frame = capture.read()
        if ret is False:
            break
        video_writer.write(frame)
    for i in range(3):
        for image_path in image_list:
            image = cv2.imread(image_path)
            video_writer.write(image)
    video_writer.release()
    shutil.rmtree('tmp/video/')
if __name__ == '__main__':
    image_list = VideoToImage(r"D:\PycharmProjects\Gitlab\samples\NJHG\data\baggage_detection\test.mp4")
    ImageToVideo(r"D:\PycharmProjects\Gitlab\samples\NJHG\data\baggage_detection\test.mp4",image_list,"test.avi")

