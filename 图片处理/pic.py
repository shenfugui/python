# -*- encoding: utf-8 -*-
# @ModuleName: pic.py
# @Author: shenfugui
# @Email: shenge_ziyi@163.com
# @Time: 2020/4/9 9:00

from PIL import Image

pic = Image.open('./1.jpg',mode="r")
print('图像的格式：',pic.format)
print('图像的大小：',pic.size)
print('图像的宽度：',pic.width)
print('图像的高度：',pic.height)
# 传入坐标的元组
print('获取某个像素点的颜色值：',pic.getpixel((100,100)))
