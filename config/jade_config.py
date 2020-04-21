#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : jade_config.py
# @Author  : jade
# @Date    : 20-4-17 下午2:01
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
from jade import Logger
import os
DEBUG = "debug"
ERROR = "ERROR"
MAXBUFFERSIZE = 1024
ROOTPATH = os.path.abspath('.')
Log = Log = Logger(ROOTPATH+'/Log.log', level=DEBUG)