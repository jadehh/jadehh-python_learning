#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_opencv_record_video_camera.py
# @Author  : jade
# @Date    : 20-6-22 上午10:40
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
from multiprocessing import Process,Queue
from jade import *

class read_video(Process):
    def __init__(self,video_path,framequeue):
        self.video_path = video_path
        self.framequeue = framequeue
        Process.__init__(self)
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
                self.framequeue.put([ret, frame])
            else:
                self.framequeue.put([ret, frame])
                break
class record_video(Process):
    def __init__(self,framequeue):
        self.framequeue = framequeue
        self.fourcc =  cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')



        Process.__init__(self)
    def run(self):
        self.videoWriter = cv2.VideoWriter(os.path.join("data/"+GetTimeStamp()+ ".avi"),
                                           self.fourcc, 30,
                                           (1024, 1360))
        while True:
            capture = self.framequeue.get()
            ret,frame = capture[0],capture[1]
            if ret:
                self.videoWriter.write(frame)
                print("正在存储视频,还剩 {} ".format(self.framequeue.qsize()))
            else:
                break

if __name__ == '__main__':
    framequeue = Queue(maxsize=200)
    read_video_process = read_video(video_path="rtsp://admin:samples123@192.168.35.212/h264/ch1/main/av_stream",
                                    framequeue=framequeue)
    read_video_process.start()
    record_video_process = record_video(framequeue)
    record_video_process.start()
