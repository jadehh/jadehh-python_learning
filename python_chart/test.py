#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : test.py
# @Author   : jade
# @Date     : 2022/5/9 10:18
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html

# 导入tailwindcss的CDN
external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]

# 创建Dash实例
app = dash.Dash(
    __name__,
    external_scripts=external_script,
)
app.scripts.config.serve_locally = True

# 创建数据
df = pd.DataFrame(
    {
        "Fruit": ["苹果", "橙子", "香蕉", "苹果", "橙子", "香蕉"],
        "Amount": [4.2, 1.0, 2.1, 2.32, 4.20, 5.0],
        "City": ["北京", "北京", "北京", "上海", "上海", "上海"],
    }
)

print(df)

# 水果单数
fruit_count = df.Fruit.count()
# 销售总额
total_amt = df.Amount.sum()
# 城市单数
city_count = df.City.count()
# 变量数
variables = df.shape[1]
# 柱状图1, 不同水果不同城市的销售额
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# 箱型图1, 不同城市的销售额分布情况
fig1 = px.box(df, x="City", y="Amount", color="City")
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

if __name__ == '__main__':
    # debug模式, 端口7777
    app.run_server(debug=True, threaded=True, port=7777)
    # 正常模式, 网页右下角的调试按钮将不会出现
    # app.run_server(port=7777)

