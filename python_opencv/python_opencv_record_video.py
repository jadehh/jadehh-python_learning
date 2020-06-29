#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_opencv_record_video.py
# @Author  : jade
# @Date    : 20-4-27 下午3:58
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
from multiprocessing import Process,Queue
from jade import *
import argparse
class read_video(Process):
    def __init__(self,video_path,framequeue):
        self.video_path = video_path
        self.framequeue = framequeue
        Process.__init__(self)
    def run(self):
        print(self.video_path)
        capture = cv2.VideoCapture(self.video_path)

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
    def __init__(self,framequeue,channel,Day,StartTime):
        self.framequeue = framequeue
        self.channel = int(channel[0:1])
        self.day = Day
        self.start_time = StartTime
        self.fourcc =  cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')



        Process.__init__(self)
    def run(self):

        if self.channel == 1:
            self.videoWriter = cv2.VideoWriter(os.path.join("/home/jade/Data/TaiCang/Container/" + self.day + "/front/", self.start_time + ".avi"), self.fourcc, 30,
                                               (1920, 1080))
        if self.channel == 2:
            self.videoWriter = cv2.VideoWriter(os.path.join("/home/jade/Data/TaiCang/Container/" + self.day + "/back/", self.start_time + ".avi"), self.fourcc, 30,
                                               (1920, 1080))


        if self.channel == 3:  ##3是后箱号 6左边箱号,1前箱号
            self.videoWriter = cv2.VideoWriter(os.path.join("/home/jade/Data/TaiCang/Container/" + self.day + "/left/", self.start_time + ".avi"), self.fourcc, 30,
                                               (2048, 1536))

        while True:
            capture = self.framequeue.get()
            ret,frame = capture[0],capture[1]
            if ret:
                self.videoWriter.write(frame)
                print("{} 正在存储视频 shape = {} ".format(self.channel,frame.shape))
            else:
                break

def start_record(args):
    start_time = args.s
    duration = args.e

    hour = start_time[:2]
    miniute = start_time[2:4]
    second = start_time[4:]
    if second == "00":
        second_int = 0
    elif second[:1] == "0":
        second_int = int(second[1:])
    else:
        second_int = int(second)


    if miniute == "00":
        miniute_int = 0
    elif miniute[:1] == "0":
        miniute_int = int(miniute[1:])
    else:
        miniute_int = int(miniute)

    if hour[:1] == "0":
        hour_int = int(hour[1:])
    else:
        hour_int = int(hour)



    end_time_second = int(duration) + second_int

    end_time = "{}{}{}"

    if end_time_second > 59:
        end_minute_int = miniute_int + 1
        end_time_second = end_time_second - 60
    else:
        end_minute_int = miniute_int

    if end_minute_int > 59:
        end_hour_int = hour_int + 1
        end_minute_int = end_minute_int - 60
    else:
        end_hour_int = hour_int

    if end_time_second < 10:
        end_secont = "0"+str(end_time_second)
    else:
        end_secont = str(end_time_second)

    if end_minute_int < 10:
        end_minute = "0" + str(end_minute_int)
    else:
        end_minute = str(end_minute_int)

    if end_hour_int < 10:
        end_hour = "0" + str(end_hour_int)
    else:
        end_hour = str(end_hour_int)

    end_time  = end_time.format(end_hour,end_minute,end_secont)


    video_path = "rtsp://admin:samples123@192.168.35.190:554/Streaming/tracks/{}?starttime=2020{}t{}z&endtime=2020{}t{}z"

    channels = ["101","201","301"] ##后箱号 左边箱号,前箱号
    CreateSavePath("data")
    day = "2020"+"-{}-{}".format(args.d[0:2],args.d[2:4])
    CreateSavePath("/home/jade/Data/TaiCang/Container/"+day+"/left/")
    CreateSavePath("/home/jade/Data/TaiCang/Container/"+day+"/back/")
    CreateSavePath("/home/jade/Data/TaiCang/Container/"+day+"/front/")

    framequeues = [Queue(maxsize=200) for _ in ["1"] * len(channels)]
    for i in range(len(channels)):
        read_video_process = read_video(video_path.format(channels[i], args.d, start_time, args.d, end_time), framequeues[i])
        read_video_process.start()
        record_video_process = record_video(framequeues[i], channels[i], day, "{}-{}-{}-{}".format(day,args.s[0:2],args.s[2:4], args.s[4:6]))
        record_video_process.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str,help = 'please select day')
    parser.add_argument('-s',type=str,help='please select starttime')
    parser.add_argument('-e',type=str,help="please select duration")
    args = parser.parse_args()
    print(args.d ,args.s,args.e)
    start_record(args)


