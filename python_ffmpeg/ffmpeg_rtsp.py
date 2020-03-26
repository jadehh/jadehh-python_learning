#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : ffmpeg_rtsp.py
# @Author   : jade
# @Date     : 2020/3/26 14:36
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import ffmpeg
import socket
import numpy as np
input_args = {
    "rtsp_transport":'tcp',
}
output_args = {
    "vcodec": "hevc_nvenc",
    "c:v": "hevc_nvenc",
    "pix_fmt":'rgb24',
    "format":'rawvideo'
}



process = (
    ffmpeg
    .input('rtsp://admin:samples123@192.168.35.119:554/Streaming/tracks/201?starttime=20200116t105450z&endtime=20200117t170000z',**input_args)
    .output('pipe:',**output_args)
    .run_async(pipe_stdout=True)
)

while process.poll() is None:
    in_bytes = process.stdout.read(1920 * 1080 * 3)
    try:
        image = np.frombuffer(in_bytes, np.uint8).reshape([-1, 1920, 1080, 3])
        print(image)
    except socket.error:
        process.stdout.close()
        process.wait()
        break