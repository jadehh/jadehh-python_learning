#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ffmpeg_rtsp_process.py
# @Author  : jade
# @Date    : 20-3-26 下午3:04
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
import ffmpeg
from multiprocessing import Process,Queue
import cv2


packet_size = 1920*1080*3
import numpy as np
import socket
class VideoRead(Process):
    def __init__(self,video_path,framequeue:Queue):
        self.video_path = video_path
        self.framequeue = framequeue
        Process.__init__(self)

    def run(self):
        input_args = {
            "rtsp_transport": 'tcp',
        }
        output_args = {
            "vcodec": "hevc_nvenc",
            "c:v": "hevc_nvenc",
            "pix_fmt": 'rgb24',
            "format": 'rawvideo'
        }
        self.process = (
            ffmpeg.input(self.video_path).output('-', **output_args).run_async(pipe_stdout=True)
        )

        while True:
            packet = self.process.stdout.read(packet_size)
            image = np.frombuffer(packet, np.uint8).reshape([1920, 1080, 3])
            cv2.imshow("result",image)
            cv2.waitKey(0)
            print(image)
            try:
                pass
            except socket.error:
                print('ERROR')


if __name__ == '__main__':
    framequeue = Queue(maxsize=10)
    videoRead = VideoRead("rtsp://admin:samples123@192.168.35.119:554/Streaming/tracks/201?starttime=20200116t105450z&endtime=20200117t170000z",framequeue)
    videoRead.start()