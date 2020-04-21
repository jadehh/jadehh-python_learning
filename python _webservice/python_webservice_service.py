#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_webservice_service.py
# @Author  : jade
# @Date    : 20-4-1 下午12:09
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
import soaplib
from soaplib.core.service import rpc, DefinitionBase
from soaplib.core.model.primitive import String, Integer, Boolean
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
from soaplib.core.service import soap
from soaplib.core.model.clazz import ClassModel
import json

class Rules(ClassModel):
    __namespace__ = "Rules"
    ReqSeq = String


class HelloWorldService(DefinitionBase):
    def __init__(self):
        self.a = ""
        DefinitionBase.__init__(self.environ)
    @soap(String, Integer, _returns=Array(String))
    def say_hello(self, name, times):
        results = []
        for i in range(0, times):
            results.append('Hello, %s' % name)
        return results

    @soap(Rules, _returns=Boolean)
    def get_recommend(self, rules):
        print(rules.ReqSeq)
        result = {"RecoResult":"0","ContaNoF":"CNAU1234567","ContaModelF":"22G1","ContaDoorPosiF":"1","ContaPicbs64F":"","ContaNoB":"CNAU1234568",\
        "ContaModelB":"22G1","ContaPicbs64B":"","ContaDoorPosiB":"1"}
        result = json.dumps(result)
        print(result)
        return result
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    ws = HelloWorldService()
    soap_app = soaplib.core.Application([HelloWorldService], 'tns')  # （中括号伪服务类的名称）
    wsgi_app = wsgi.Application(soap_app)
    print 'listening on 127.0.0.1:7789'
    print 'wsdl is at: http://127.0.0.1:7789/SOAP/?wsdl'
    server = make_server('0.0.0.0', 7789, wsgi_app)
    server.serve_forever()
