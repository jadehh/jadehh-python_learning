#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : tornado_server.py
# @Author   : jade
# @Date     : 2021/9/4 17:21
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import tornado
from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler,HTTPError
from threading import  Thread
import  time
import cv2
import numpy as np
import json
import requests

from concurrent.futures import ThreadPoolExecutor


class Executor(ThreadPoolExecutor):
    """ 创建多线程的线程池，线程池的大小为10
    创建多线程时使用了单例模式，如果Executor的_instance实例已经被创建，
    则不再创建，单例模式的好处在此不做讲解
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=10)
        return cls._instance


class OCR(RequestHandler):
    executor = Executor()

    @tornado.web.asynchronous  # 异步处理
    @tornado.gen.coroutine  # 使用协程调度
    def post(self, *args, **kwargs):
        """
        只支持body传参
        """
        token = self.get_body_arguments('token')[0]
        image_shape = self.get_body_arguments("image_shape")[0]
        image_data = self.request.files["image_data"][0]["body"]
        result = yield self._process()
        self.write(result)


    @tornado.concurrent.run_on_executor  # 增加并发量
    def _process(self):
        # 此处执行具体的任务
        return 'success'



class HttpServer(object):
    def __init__(self,port):
        self.port = port
        super(HttpServer, self).__init__()
    def StartServerThread(self):
        self.thread = Thread(target=self.StartServer)
        self.thread.start()
    def StartServer(self):
        self.app = Application([(r"/ocr", OCR)])
        http_server = HTTPServer(self.app)
        http_server.listen(self.port)
        ioloop.IOLoop.instance().start()

class TESTProcess(Thread):
    def __init__(self,index,datas,image):
        self.index=index
        self.datas = datas
        self.image = image
        Thread.__init__(self)

    def run(self):
        r = requests.post("http://localhost:8001/ocr", data=self.datas, files={"image_data": (self.image.tobytes())},headers={"Connection":"close"})

        print(self.index,r.text)


if __name__ == '__main__':
    httpServer = HttpServer(8001)
    httpServer.StartServerThread()
    print("服务启动完成")

    for i in range(1000000):
        datas = {"token": 123,
                 "image_shape": "{},{},{}".format(1,2,3)}
        testProcess = TESTProcess(i, datas=datas, image=np.array([1,2,3]))
        testProcess.start()


