#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : opencv_record_fps.py
# @Author   : jade
# @Date     : 2021/6/24 14:41
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from jade import *

class read_video(Thread):
    def __init__(self, video_path, framequeue):
        self.video_path = video_path
        self.framequeue = framequeue
        Thread.__init__(self)

    def run(self):
        print(self.video_path)
        capture = cv2.VideoCapture(self.video_path)

        if capture.isOpened():
            print("read success")
        else:
            print("read failure")
        while capture.isOpened():
            ret, frame = capture.read()
            if ret:
                self.framequeue.put((ret,frame))
            else:
                self.framequeue.put((ret,frame))
                break


class record_video(Thread):
    def __init__(self, framequeue, path,fps):
        self.framequeue = framequeue
        self.fps = fps
        self.save_path =GetPreviousDir(path) + "/" + GetTime()+ "_{}.avi".format(fps)
        self.fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

        Thread.__init__(self)

    def run(self):
        ret,frame = self.framequeue.get()
        self.videoWriter = cv2.VideoWriter(self.save_path,self.fourcc, self.fps, (frame.shape[1], frame.shape[0]))
        while True:
            ret, frame = self.framequeue.get()
            if ret:
                self.videoWriter.write(frame)
                print("正在存储视频 shape = {} ".format(frame.shape))
            else:
                break

def start_record(args):
    framequeue = Queue(100)
    read_video_process = read_video(args.path,
                                        framequeue)
    read_video_process.start()
    record_video_process = record_video(framequeue,args.path,args.fps)
    record_video_process.start()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, help='please select video path',required=True)
    parser.add_argument('-fps', type=int, help='please select video fps',required=True)
    args = parser.parse_args()
    start_record(args)
