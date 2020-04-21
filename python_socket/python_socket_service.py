#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_socket_service.py
# @Author  : jade
# @Date    : 20-4-17 下午1:56
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
from config.jade_config import *
from jade import JadeLog
import socket
import threading
from multiprocessing import Process

## 接受从客户端发送的消息,需要单独开个进程
class SamplesSocketService(Process):
    def __init__(self, ip, port,func,model):
        try:
            self.socket_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
            self.socket_service.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_service.bind((ip, port))
            self.socket_service.listen(20)
            self.func = func
            self.model = model
            JadeLog(Log,"Establish a short connection, IP Address = {},port = {}, to connect the backstage".format(ip, port),INFO)
        except socket.error as msg:
            JadeLog(Log, "ERROR msg = {}".format(msg), ERROR)

        Process.__init__(self)
    def deal_data(self,conn,addr):
        data = b''
        while True:
            data_tmp = conn.recv(MAXBUFFERSIZE)
            if data_tmp:
                data = data + data_tmp
            else:
                break
        self.func(data,self.model)
        ##将这个data回调出去

    def run(self):
        while True:
            conn, addr = self.socket_service.accept()
            t = threading.Thread(target=self.deal_data, args=(conn, addr))
            t.start()


if __name__ == '__main__':
    socketService = SamplesSocketService('192.168.40.192', 8080)
    socketService.run()