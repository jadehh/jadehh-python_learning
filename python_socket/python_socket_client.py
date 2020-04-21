#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_socket_client.py
# @Author  : jade
# @Date    : 20-4-17 下午2:00
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
from jade import JadeLog
from config.jade_config import *
import socket
import struct
import binascii
class SocketClient():
    def __init__(self,ip,port):
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            JadeLog(Log,"Connect to IP = {},Port = {}".format(ip,port),DEBUG)
            self.socket_client.connect((ip, port))
            self.isConnect = True
        except socket.error as msg:
            self.isConnect = False
            JadeLog(Log,"ERROR,Connect to IP = {},Port = {}".format(ip,port),ERROR)
            # sys.exit(1)

    def sendMsg(self, data, writeable=True):
        if self.isConnect:
            if writeable:
                JadeLog(Log,"Send Message,the data is  {}".format(data),DEBUG)
            self.socket_client.send(data)



class SocketData:
    def __init__(self,data):
        ##需要判断消息类型,不同的消息类型,后面报文的内容不一样
        self.pack_msg_type = binascii.b2a_hex(data[8:9])
        self.pack_length = data[4:8]
        self.pack_head_byte = data[:38]
        self.pack_content_byte = data[38:-2]
        self.pack_tail_byte = data[-2:]
        self.pack_head_sign_byte = self.pack_head_byte[:4]
        self.pack_arrival_number = self.pack_head_byte[9:19]
        self.pack_channel_number = self.pack_head_byte[19:29]
        self.pack_exits_entrances_sign = self.pack_head_byte[29:30]
        self.pack_designer = self.pack_head_byte[30:34]
        self.pack_xml_lenght = self.pack_head_byte[34:38]

    def setMsgType(self,msg_type):
        return self.pack_head_byte[:8] + msg_type + self.pack_head_byte[9:]

    def setAllLength(self,byte):

        return byte[:4] +struct.pack("<I", len(byte)) + byte[8:34] +struct.pack("<I", len(byte)-40) + byte[38:]

    def getContent(self):
         return self.pack_content_byte.decode(encoding="gb2312")


    def setSeqNumber(self,seqNumber):
        xml_content = self.getContent()
        xml_content_head  = xml_content.split("SEQ_NO=")[0] + "SEQ_NO="
        xml_content_context = "\"" + str(seqNumber) + "\"" + ">\n"
        xml_content_tail = '<EXT>\n' \
                      '<I_E_TIME>2019-12-24 16:32:14</I_E_TIME>\n' \
                      '<PIC_LIST>\n<PIC name="YC_T">ftp://jade:jade@192.168.40.192/share/images/2019-12-24/top/2019-12-24-16-32-14.jpg</PIC>\n' \
                      '</PIC_LIST>\n</EXT></GATHER_INFO>'
        xml_content = xml_content_head + xml_content_context + xml_content_tail
        return self.pack_head_byte + xml_content.encode()+ self.pack_tail_byte