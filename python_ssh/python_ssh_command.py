#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_ssh_command.py
# @Author   : jade
# @Date     : 2021/6/20 14:14
# @Email    : jadehh@1ive.com
# @Software : Samples
import paramiko
from paramiko.sftp_client import SFTPClient
import os
import shutil
class SSHService():
    def __init__(self, ip_address, username, passwd):
        self.ip_address = ip_address
        self.username = username
        self.passwd = passwd
        self.is_connect = False
        self.des = ""
        self.connect()

    def connect(self):
        self.ssh = paramiko.SSHClient()  # 创建SSH对象
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
        try:
            self.ssh.connect(hostname=self.ip_address, port=22, username=self.username, password=self.passwd)  # 连接服务器
            self.is_connect = True
        except Exception as e:
            self.is_connect = False
            self.des = e

    def copy_files(self,ftpclient,dir,remotefile):
        if os.path.isdir(dir):
            for filename in os.listdir(dir):
                if os.path.isdir(os.path.join(dir,filename)):
                    self.run_cmd("mkdir {}".format(remotefile + "/{}".format(filename)))
                    self.copy_files(ftpclient,os.path.join(dir,filename),remotefile + "/{}".format(filename))
                else:
                    ftpclient.put("{}/{}".format(dir,filename),"{}/{}".format(remotefile,filename))
        else:
            return

    def copyFiles(self,localfile,remotefile):
        if self.is_connect:
            ftp_client:SFTPClient = self.ssh.open_sftp()
            self.run_cmd("mkdir {}".format(remotefile))
            try:
                self.copy_files(ftp_client,localfile,remotefile)
            except Exception as e:
                return "ERROR,上传失败,失败原因为{}".format(e)
        else:
            return "ERROR:ssh连接失败,失败原图{}".format(self.des)

    def copy(self,localfile,remotefile):
        if self.is_connect:
            ftp_client = self.ssh.open_sftp()
            try:
                ftp_client.put(localfile,remotefile)
            except Exception as e:
                return "ERROR,上传失败,失败原因为{}".format(e)
        else:
            return "ERROR:ssh连接失败,失败原图{}".format(self.des)

    def get_home_path(self):
        if self.is_connect:
            stdin, stdout, stderr = self.ssh.exec_command("pwd")
            res, err = stdout.read(), stderr.read()
            result = str(res if res else err, encoding="utf-8")
            return result.split("\n")[0]
        else:
            return "ERROR:ssh连接失败,失败原图{}".format(self.des)

    def run_cmd(self, cmd_str):
        if self.is_connect:
            stdin, stdout, stderr = self.ssh.exec_command(cmd_str)
            res, err = stdout.read(), stderr.read()
            result = str(res if res else err, encoding="utf-8")
            return result
        else:
            return "ERROR:ssh连接失败,失败原图{}".format(self.des)

    def welcome(self):
        if self.is_connect:
            stdin, stdout, stderr = self.ssh.exec_command('cd /etc/update-motd.d && bash *')  # 执行命令并获取命令结果
            res, err = stdout.read(), stderr.read()
            result = str(res if res else err, encoding="utf-8")
            self.ssh.close()
            return "ssh连接\n" + result
        else:
            return "ERROR:ssh连接失败,失败原图{}".format(self.des)

    def listdir(self, target_path):
        if self.is_connect:
            ftp_client = self.ssh.open_sftp()
            try:
                file_list = ftp_client.listdir(target_path)
                return file_list
            except Exception as e:
                return []
        else:
            return "ERROR:ssh连接失败,失败原图{}".format(self.des)

    def download_files(self,ftpclient,dir,localfile):
        file_list = self.listdir(dir)
        if file_list:
            for filename in self.listdir(dir):
                sec_list = self.listdir(dir+"/"+filename)
                if sec_list:
                    os.mkdir("{}".format(localfile + "/{}".format(filename)))
                    self.download_files(ftpclient, dir+"/"+filename, localfile + "/{}".format(filename))
                else:
                    ftpclient.get("{}/{}".format(dir, filename), "{}/{}".format(localfile, filename))

        else:
            return
    def downloadFiles(self,remotefile,localfile):
        if self.is_connect:
            ftp_client = self.ssh.open_sftp()
            if os.path.exists(localfile):
               shutil.rmtree(localfile)
               os.makedirs(localfile)
            else:
                os.makedirs(localfile)
            try:
                self.download_files(ftp_client,remotefile,localfile)
            except Exception as e:
                return "ERROR,上传失败,失败原因为{}".format(e)
        else:
            return "ERROR:ssh连接失败,失败原图{}".format(self.des)

    def download(self,remotefile,localfile):
        if self.is_connect:
            ftp_client = self.ssh.open_sftp()
            try:
                ftp_client.get(remotefile,localfile)
            except Exception as e:
                return "ERROR,上传失败,失败原因为{}".format(e)
        else:
            return "ERROR:ssh连接失败,失败原图{}".format(self.des)

    def close(self):
        self.ssh.close()

if __name__ == '__main__':
    SSHClient = SSHService("192.168.35.120","samples","samples@123")
    SSHClient.downloadFiles("/home/samples/sda2/container_ocrV2.2-1","container_ocrV2.2-1")
