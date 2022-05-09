#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : ffmpeg_rtsp.py
# @Author   : jade
# @Date     : 2020/3/26 14:36
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import cv2
import ffmpeg
import numpy as np
cv2.VideoCapture()
class Capture(object):
    def __init__(self,pipe,width,height):
        self.pipe = pipe
        self.width  = width
        self.height = height
    def isOpened(self):
        if self.pipe is None:
            return False
        else:
            return True
    def read(self):
        if self.isOpened() is None:
            return False, None
        else:
            in_bytes = self.pipe.stdout.read(self.width * self.height * 3)
            if len(in_bytes) == 0:
                return False, None
            else:
                image = (
                    np.frombuffer(in_bytes, np.uint8)
                        .reshape([self.height, self.width, 3])
                )
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                return True, image

class FFMpegCapture(object):
    def __init__(self):
        super(FFMpegCapture, self).__init__()
    def VideoCapute(self,video_path):
        try:
            probe = ffmpeg.probe(video_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            self.width = int(video_info['width'])
            self.height = int(video_info['height'])
            self.out = (
            ffmpeg
                .input(video_path)
                .output('pipe:', format='rawvideo', pix_fmt='rgb24')
                .run_async(pipe_stdout=True)
            )
            return Capture(self.out,self.width,self.height)
        except Exception as e:
            print(e)
            return Capture(None,None,None)






if __name__ == '__main__':
    capture = FFMpegCapture().VideoCapute("rtmp://192.168.43.150:10054/live/AZXdMnc7R")
    if capture.isOpened():
        print("相机打开成功")
    else:
        print("相机打开失败")
    while capture.isOpened():
        ret,frame = capture.read()
        if ret is False:
            break
        cv2.imshow("result",frame)
        cv2.waitKey(1)