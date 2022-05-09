#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : pyqt_url.py
# @Author   : jade
# @Date     : 2022/5/9 11:13
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from threading import Thread
class HttpThread(Thread):
    def __init__(self):
        self.external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
        self.prepare_data()
        super(HttpThread, self).__init__()
    def prepare_data(self):
        # 创建数据
        self.df = pd.DataFrame(
            {
                "Fruit": ["苹果", "橙子", "香蕉", "苹果", "橙子", "香蕉"],
                "Amount": [4.2, 1.0, 2.1, 2.32, 4.20, 5.0],
                "City": ["北京", "北京", "北京", "上海", "上海", "上海"],
            }
        )

    def paint_html(self,app):
        fig, fig1 = self.paint_chart()
        # 水果单数
        fruit_count = self.df.Fruit.count()
        # 销售总额
        total_amt = self.df.Amount.sum()
        # 城市单数
        city_count = self.df.City.count()
        # 变量数
        variables = self.df.shape[1]
        app.layout = html.Div(
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H1(children="水果销售--可视化报表", className=" py-3 text-5xl font-bold text-gray-800"),
                            html.Div(
                                children="""Python with Dash = 💝 .""",
                                className="text-left prose prose-lg text-2xl  py-3 text-gray-600",
                            ),
                        ],
                        className="w-full mx-14 px-16 shadow-lg bg-white -mt-14 px-6 container my-3 ",
                    ),
                    html.Div(
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        f"¥{total_amt}",
                                        html.Br(),
                                        html.Span("总销售额", className="text-lg font-bold ml-4"),
                                    ],
                                    className=" shadow-xl py-4 px-14 text-5xl bg-[#76c893] text-white  font-bold text-gray-800",
                                ),
                                html.Div(
                                    children=[
                                        fruit_count,
                                        html.Br(),
                                        html.Span("水果数量", className="text-lg font-bold ml-4"),
                                    ],
                                    className=" shadow-xl py-4 px-24 text-5xl bg-[#1d3557] text-white  font-bold text-gray-800",
                                ),
                                html.Div(
                                    children=[
                                        variables,
                                        html.Br(),
                                        html.Span("变量", className="inline-flex items-center text-lg font-bold ml-4"),
                                    ],
                                    className=" shadow-xl py-4 px-24 text-5xl bg-[#646ffa] text-white  font-bold text-gray-800",
                                ),
                                html.Div(
                                    children=[
                                        city_count,
                                        html.Br(),
                                        html.Span("城市数量", className="text-lg font-bold ml-4"),
                                    ],
                                    className="w-full shadow-xl py-4 px-24 text-5xl bg-[#ef553b] text-white  font-bold text-gray-800",
                                ),
                            ],
                            className="my-4 w-full grid grid-flow-rows grid-cols-1 lg:grid-cols-4 gap-y-4 lg:gap-[60px]",
                        ),
                        className="flex max-w-full justify-between items-center ",
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    dcc.Graph(id="example-graph", figure=fig),
                                ],
                                className="shadow-xl w-full border-3 rounded-sm",
                            ),
                            html.Div(
                                children=[
                                    dcc.Graph(id="example-graph1", figure=fig1),
                                ],
                                className="w-full shadow-2xl rounded-sm",
                            ),
                        ],
                        className="grid grid-cols-1 lg:grid-cols-2 gap-4",
                    ),
                ],
                className="bg-[#ebeaee]  flex py-14 flex-col items-center justify-center ",
            ),
            className="bg-[#ebeaee] container mx-auto px-14 py-4",
        )



    def paint_chart(self):
        # 柱状图1, 不同水果不同城市的销售额
        fig = px.bar(self.df, x="Fruit", y="Amount", color="City", barmode="group")

        # 箱型图1, 不同城市的销售额分布情况
        fig1 = px.box(self.df, x="City", y="Amount", color="City")
        return fig,fig1

    def run(self):
        app = dash.Dash(
            __name__,
            external_scripts=self.external_script,
        )
        app.scripts.config.serve_locally = True
        self.paint_html(app)
        # debug模式, 端口7777
        # app.run_server(debug=True, threaded=False, port=7777)
        # 正常模式, 网页右下角的调试按钮将不会出现
        app.run_server(port=7777)










class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('chart')  #窗口标题
        self.setGeometry(5,30,1355,730)  #窗口的大小和位置设置
        self.browser=QWebEngineView()
        #加载外部的web界面
        self.browser.load(QUrl('http://127.0.0.1:7777/'))
        self.setCentralWidget(self.browser)
if __name__ == '__main__':
    httpThread = HttpThread()
    httpThread.start()
    app=QApplication(sys.argv)
    win=MainWindow()
    win.show()
    app.exit(app.exec_())