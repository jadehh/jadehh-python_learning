#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : pyqt_html.py
# @Author   : jade
# @Date     : 2022/5/9 10:57
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('测试Html')  #窗口标题
        self.setGeometry(5,30,1355,730)  #窗口的大小和位置设置
        self.browser=QWebEngineView()
        # 加载html代码(这里注意html代码是用三个单引号包围起来的)
        self.browser.setHtml('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div id="app">
        <span>我在#app里面{{a}}</span>
    </div>
    <span>我不在#app里面{{a}}</span>
</body>
</html>
<!-- 利用cdn引入vue -->
<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
<script>
    new Vue({
        el:'#app', 
        /*el:'#app'，容器选择器，只能匹配到第一个满足条件的，相当于document.querySeleceor()，
          可以是#app，对应id名为app，也可以是.app，对象的class名为app，也可以是标签名
          即el:'div'
          注意事项：容器选择器不能选择到body或者html标签，
          且这个new Vue出来的只对容器选择器里的所有内容起作用
        */
        data:{
        	//要用的数据都放在这里
            a:'我是一个span标签！'
        }
    })
</script>
''')
        self.setCentralWidget(self.browser)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=MainWindow()
    win.show()
    app.exit(app.exec_())