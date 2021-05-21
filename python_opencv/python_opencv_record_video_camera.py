#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_opencv_record_video_camera.py
# @Author  : jade
# @Date    : 20-6-22 上午10:40
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
from threading import Thread
from queue import Queue

from jade import *

class read_video(Thread):
    def __init__(self,video_path,framequeue):
        self.video_path = video_path
        self.framequeue = framequeue
        self.index = 0
        Thread.__init__(self)
    def run(self):
        capture = cv2.VideoCapture(self.video_path)
        print(self.video_path)
        if capture.isOpened():
            print("read success")
        else:
            print("read failure")
        while capture.isOpened():
            ret,frame = capture.read()
            if ret:
                if self.index % 10 == 0:
                    self.framequeue.put([ret, frame])
            else:
                self.framequeue.put([ret, frame])
                break
            self.index = self.index + 1
class record_video(Thread):
    def __init__(self,framequeue):
        self.framequeue = framequeue
        self.fourcc =  cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')



        Thread.__init__(self)
    def run(self):
        capture = self.framequeue.get()
        image = capture[1]
        save_path = os.path.join("{}/data/").format(os.path.expanduser("~"))
        CreateSavePath(save_path)
        video_path = os.path.join(save_path,GetTime()+ ".avi")
        self.videoWriter = cv2.VideoWriter(video_path,self.fourcc, 20, (image.shape[1],image.shape[0]))
        while True:
            capture = self.framequeue.get()
            ret,frame = capture[0],capture[1]
            if ret:
                self.videoWriter.write(frame)
                print("正在存储视频,还剩 {} 宽 = {} 高 = {}".format(self.framequeue.qsize(),frame.shape[1],frame.shape[0]))
            else:
                break

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str,help = 'please select day')
    parser.add_argument('-username',type=str,help='please select starttime')
    parser.add_argument('-passwd',type=str,help="please select duration")
    args = parser.parse_args()
    print(args.ip ,args.username,args.passwd)

    framequeue = Queue(maxsize=200)
    read_video_process = read_video(video_path="rtsp://{}:{}@{}/h264/ch1/main/av_stream".format(args.username,args.passwd,args.ip),
                                    framequeue=framequeue)
    read_video_process.start()
    record_video_process = record_video(framequeue)
    record_video_process.start()
