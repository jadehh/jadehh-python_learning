#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_webservice_client.py
# @Author  : jade
# @Date    : 20-4-1 下午12:22
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
from suds.client import Client
hello_client = Client('http://localhost:7789/?wsdl')
hello_client.options.cache.clear()
rules={}
rules["ReqSeq"]="alle"

print rules
result = hello_client.service.get_recommend(rules)
print result