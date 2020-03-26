#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ffmpeg_video.py
# @Author  : jade
# @Date    : 20-3-26 下午3:48
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
import ffmpeg
import cv2
import numpy as np
input_args = {
    # "hwaccel": "nvdec",
    # "vcodec": "h264_cuvid",
    # "c:v": "h264_cuvid"
}

output_args = {
    "vcodec": "hevc_nvenc",
    "c:v": "hevc_nvenc",
    "pix_fmt":'rgb24',
    "format":'rawvideo'
}


process = (
    ffmpeg
    .input("/home/jade/sda2/Data/ChangZhou/192.168.35.32_01_20200310_163925/192.168.35.30_01_20200310_163918.mp4")
    .output('pipe:', **output_args)
    .run_async(pipe_stdout=True)
)



while process.poll() is None:
    in_bytes = process.stdout.read(1920 * 1080 * 3)
    print("get image")
    image = np.frombuffer(in_bytes, np.uint8).reshape([1920, 1080, 3])
    cv2.imshow("image",image)
    cv2.waitKey(0)