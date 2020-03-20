#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_opencv_process.py
# @Author  : jade
# @Date    : 20-3-19 上午9:44
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :

from multiprocessing import Process,Queue,Pipe
import cv2
import time
class VideoReadProcess(Process):
    def __init__(self,video_path,framequeue:Queue):
        self.video_path = video_path
        self.framequeue = framequeue
        Process.__init__(self)

    def run(self):
        capture = cv2.VideoCapture(self.video_path)
        while capture.isOpened():
            ret,frame = capture.read()
            self.framequeue.put([ret,frame])
            #time.sleep(0.01)

class VideoShowProcess(Process):
    def __init__(self,framequeue:Queue):
        self.framequeue = framequeue
        Process.__init__(self)
    def run(self):
        cv2.namedWindow("frame",0)
        while True:
            if self.framequeue.empty():
                time.sleep(0.1)
                continue
            [ret,frmae] = self.framequeue.get()
            cv2.imshow("frame",frmae)
            cv2.waitKey(1)





if __name__ == '__main__':
    framequeue = Queue(maxsize=5)
    videoShowProcess = VideoShowProcess(framequeue)
    videoShowProcess.start()
    print("videoShowProcess pid = {}".format(videoShowProcess.pid))
    videoReadProcess = VideoReadProcess("rtsp://admin:samples123@192.168.35.119:554/Streaming/tracks/301?starttime=20200116t105450z&endtime=20200117t170000z",framequeue)
    videoReadProcess.start()
    print("videoReadProcess pid = {}".format(videoReadProcess.pid))