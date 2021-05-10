#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : rgbrgb_rrggbb.py
# @Author   : jade
# @Date     : 2021/5/8 16:28
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import cv2
import numpy as np
import time
def array_to_image_single(arr):
    print("### numpy直接操作方法")
    start_time = time.time()
    # need to return old values to avoid python freeing memory
    arr = arr.transpose(2,0,1)
    arr = np.ascontiguousarray(arr.flat, dtype=np.float32)
    # print(arr)

    end_time = time.time() - start_time

    print(">花费了 = {} ms".format(round(end_time,4) * 1000))

def image_to_rr_gg_bb(arr):
    print("### Mat转Data遍历方法")
    start_time = time.time()
    h = arr.shape[0]
    w = arr.shape[1]
    c = arr.shape[2]
    arr = np.ascontiguousarray(arr.flat, dtype=np.float32)
    data = np.zeros(h*w*c)
    for i in range(h*w*c):
        if i % 3 == 0:
            data[int(i/3)] = arr[i]
        elif i % 3 == 1:
            data[int(i/3)+h*w] = arr[i]
        elif i % 3 == 2:
            data[int(i/3)+h*w*2] = arr[i]



    end_time = time.time()-start_time

    print(">花费了 = {} ms".format(round(end_time,4) * 1000))



def mat_to_image(arr):
    print("### Mat遍历矩阵方法")
    start_time = time.time()
    h = arr.shape[0]
    w = arr.shape[1]
    c = arr.shape[2]
    data = [0]*h*w*c
    for i in range(h):
        for j in range(w):
            for k in range(c):
                data[k * w * h + i * w + j] = arr[i,j,k]
    data = np.array(data,dtype=np.float)
    # print(data)

    end_time = time.time() - start_time

    print(">花费了 = {} ms".format(round(end_time,4) * 1000))


def printMat(arr):
    print("|      |      |      |      |      |      |      |      |      |      |\n"
          "| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |")

    for i in range(arr.shape[0]):
        str = "|"
        for j in range(arr.shape[1]):
            for k in range(arr.shape[2]):
                if k == arr.shape[2]-1:
                    str = str + "{}".format(arr[i, j, k])
                else:
                    str = str + "{},".format(arr[i, j, k])
            str = str + "|"
        str = str + "|"
        print(str)

if __name__ == '__main__':
    image = cv2.imread("/mnt/f/测试集/416_416图片/result.jpg")
    # image = cv2.resize(image, (10, 10))
    print("### 测试一张分辨率为{}*{}的图片".format(image.shape[1],image.shape[0]))
    array_to_image_single(image)
    mat_to_image(image)
    image_to_rr_gg_bb(image)

