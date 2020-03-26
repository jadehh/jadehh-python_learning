#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : ffmpeg_rtsp.py
# @Author   : jade
# @Date     : 2020/3/26 14:36
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import ffmpeg
packet_size = 4096

process = (
    ffmpeg
    .input('rtsp://admin:samples123@192.168.35.119:554/Streaming/tracks/201?starttime=20200116t105450z&endtime=20200117t170000z')
    .output('-', format='h264')
    .run_async(pipe_stdout=True)
)

while process.poll() is None:
    packet = process.stdout.read(packet_size)
    try:
        tcp_socket.send(packet)
    except socket.error:
        process.stdout.close()
        process.wait()
        break