#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_ftp_download.py
# @Author   : jade
# @Date     : 2021/6/10 13:50
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
"""
FTP常用操作
"""
from ftplib import FTP
import os
class FTP_OP(object):
    def __init__(self, host, username, password, port):
        """
        初始化ftp
        :param host: ftp主机ip
        :param username: ftp用户名
        :param password: ftp密码
        :param port:  ftp端口 （默认21）
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
    def ftp_connect(self):
    """
    连接ftp
    :return:
    """
    ftp = FTP()
    ftp.set_debuglevel(0)  # 不开启调试模式
    ftp.connect(host=self.host, port=self.port)  # 连接ftp
    ftp.login(self.username, self.password)  # 登录ftp
    return ftp
    def download_file(self, ftp_file_path, dst_file_path):
    """
    从ftp下载文件到本地
    :param ftp_file_path: ftp下载文件路径
    :param dst_file_path: 本地存放路径
    :return:
    """
    buffer_size = 10240  #默认是8192
    ftp = self.ftp_connect()
    print (ftp.getwelcome())  #显示登录ftp信息
    file_list = ftp.nlst(ftp_file_path)
    for file_name in file_list:
        ftp_file = os.path.join(ftp_file_path, file_name)
        write_file = os.path.join(dst_file_path, file_name)
        print (file_name)
        if file_name.find('.jpg')>-1 and not os.path.exists(write_file):
            print ("file_name:"+file_name)
            #ftp_file = os.path.join(ftp_file_path, file_name)
            #write_file = os.path.join(dst_file_path, file_name)
            with open(write_file, "wb") as f:
                ftp.retrbinary('RETR {0}'.format(ftp_file), f.write, buffer_size)
                f.close()
    ftp.quit()

if __name__ == '__main__':
    host = "10.201.xx.xx"
    username = "xxx"
    password = "xxx"
    port = "9999"
    ftp_file_path = "/upload/20160726"
    dst_file_path = "/home/gdmt/master/py/tmp"
    ftp = FTP_OP(host=host, username=username, password=password, port=port)
    ftp.download_file(ftp_file_path=ftp_file_path, dst_file_path=dst_file_path)