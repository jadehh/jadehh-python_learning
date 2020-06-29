#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : python_load_mnist.py
# @Author  : jade
# @Date    : 20-5-28 下午5:42
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :
import os
import struct
import numpy as np
import cv2
def load_mnist(path, kind='train'):
    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,
                               '%s-labels.idx1-ubyte'
                               % kind)
    images_path = os.path.join(path,
                               '%s-images.idx3-ubyte'
                               % kind)


    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II',
                                 lbpath.read(8))
        labels = np.fromfile(lbpath,
                             dtype=np.uint8)

    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII',
                                               imgpath.read(16))
        images = np.fromfile(imgpath,
                             dtype=np.uint8).reshape(len(labels), 784)


    for i in range(len(images)):
        image = images[i]
        image = np.resize(image,[28,28,1])
        cv2.imwrite("{}.pgm".format(labels[i]),image)


    return images, labels



if __name__ == '__main__':
    load_mnist("/home/jade/sda2/Data/mnist","t10k")