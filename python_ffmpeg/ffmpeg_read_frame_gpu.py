#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ffmpeg_read_frame_gpu.py
# @Author  : jade
# @Date    : 20-3-26 下午4:49
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
import cv2
import ffmpeg
import numpy as np
from PIL import Image
from io import BytesIO
input_args = {
    "rtsp_transport":'tcp',
    # "c:v": "h264_cuvid",
    # "vsync": "0",
    # "hwaccel":"cuvid"
}
output_args = {
    "pix_fmt":'bgr24',
    "format":'rawvideo'
}

file_name = "rtsp://admin:samples123@192.168.35.119:554/Streaming/tracks/201?starttime=20200116t105450z&endtime=20200117t170000z"
probe = ffmpeg.probe(file_name)
video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
width = int(video_info['width'])
height = int(video_info['height'])
out = (
    ffmpeg
    .input(file_name,**input_args)
    .output('pipe:',**output_args)
    .run_async(pipe_stdout=True)
)
cv2.namedWindow("result", 0)
while out.poll() is None:
    in_bytes = out.stdout.read(1920 * 1080 * 3)
    bytes_stream = BytesIO(in_bytes)
    roiimg = Image.open(bytes_stream)
    # video = (
    #     np.frombuffer(in_bytes, np.uint8)
    #         .reshape([height, width, 3])
    # )
    cv2.imshow("result", roiimg)
    cv2.waitKey(1)
