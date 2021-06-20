#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : python_ssh_command.py
# @Author   : jade
# @Date     : 2021/6/20 14:14
# @Email    : jadehh@1ive.com
# @Software : Samples
import paramiko

ssh = paramiko.SSHClient()  # 创建SSH对象
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
ssh.connect(hostname='192.168.35.120', port=22, username='samples', password='samples@123')  # 连接服务器

stdin, stdout, stderr = ssh.exec_command('docker images')  # 执行命令并获取命令结果
# stdin为输入的命令
# stdout为命令返回的结果
# stderr为命令错误时返回的结果
res, err = stdout.read(), stderr.read()
result = res if res else err
print(result)
ssh.close()  # 关闭连接

