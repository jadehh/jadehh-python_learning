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


file_name = "rtsp://admin:samples123@192.168.35.119:554/Streaming/tracks/201?starttime=20200116t105450z&endtime=20200117t170000z"
probe = ffmpeg.probe(file_name)
video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
width = int(video_info['width'])
height = int(video_info['height'])
out = (
    ffmpeg
    .input(file_name)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .run_async(pipe_stdout=True)
)
cv2.namedWindow("result", 0)
while out.poll() is None:
    in_bytes = out.stdout.read(1920 * 1080 * 3)
    video = (
        np.frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
    )
    cv2.imshow("result", video)
    cv2.waitKey(1)

