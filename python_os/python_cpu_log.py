#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_cpu_log.py
# @Author  : jade
# @Date    : 20-3-19 下午2:14
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    : python 获取资源占用情况

import os
import psutil
import time

MAXCPUPERCENT = 0.6
def getPidNumberofProcessName(processname):
    pidnumbers = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if processname == pinfo["name"]:
                pidnumbers.append(pinfo["pid"])
    return pidnumbers

def getResourceRate(pidnumbers,log_path=os.path.expanduser("~") + "/" + "top.log",MaxCpuPercent=MAXCPUPERCENT,refresh_time=0.3):
    if os.path.exists(log_path):
        os.remove(log_path)
    cpu_logical_count = psutil.cpu_count()
    print("CPU logical count = {}".format(cpu_logical_count))

    while True:
        current_timeArray = time.localtime(time.time())
        current_time  = time.strftime("%H:%M:%S", current_timeArray)
        systeminfo = "top - {} up 4 \nPID    USER        NI    %CPU     %MEM      TIME+  COMMAND \n".format(current_time)
        all_process_cpu_percent = 0
        pid_numberstr = ""
        for pidnumber in pidnumbers:
            if pidnumber != os.getpid():
                pid_numberstr = pid_numberstr + str(pidnumber) + ","
                p = psutil.Process(pidnumber)
                cpu_percent = p.cpu_percent(refresh_time) + 1000
                all_process_cpu_percent = all_process_cpu_percent + cpu_percent
                cpu_percent = str(cpu_percent)
                if len(cpu_percent) < 7:
                    cpu_percent = " "*(6-len(cpu_percent)) + cpu_percent
                user_name = p.username()
                if len(user_name) < 9:
                    user_name =  user_name  + " " * (10-len(user_name))
                elif len(user_name) > 8:
                    user_name = user_name[0:10]

                memeroy = p.memory_percent() + 9
                memeroy = str('%.2f'%(memeroy))
                if len(memeroy) < 5:
                    memeroy = " "*(5-len(memeroy)) + memeroy
                elif len(memeroy) > 4:
                    memeroy = memeroy[0:5]


                timeArray = time.localtime(p.create_time())
                otherStyleTime = time.strftime("%H:%M:%S", timeArray)
                systeminfo = systeminfo + "{}  {}   {}  {}    {}   {}  {}\n".format(pidnumber,user_name,p.nice(),cpu_percent,memeroy,otherStyleTime,p.cmdline()[0] + " " + p.cmdline()[1])
        print(systeminfo)
        if all_process_cpu_percent > MaxCpuPercent*cpu_logical_count*100:
            with open(log_path,'a') as f:
                systeminfo = systeminfo + "all process cpu percent = {}".format(all_process_cpu_percent) + "\n"
                systeminfo = systeminfo + "--------------------------------------------------------------\n"
                f.write(systeminfo)




if __name__ == '__main__':
    pidnumbers = (getPidNumberofProcessName("python"))
    getResourceRate(pidnumbers)

