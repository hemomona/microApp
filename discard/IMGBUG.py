# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : IMGBUG.py
# Time       ：2022/4/12 15:11
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：
"""

from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import AsyncImage, Image  # 加载异步图片
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
# 无kv文件


class BoxLayoutWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        image = Image(source='../data/1_图1.培养基1生长曲线.png')   # 创建异步图像
        self.add_widget(image)      # 把分散布局放到盒子布局里


class SAPP(App):
    def build(self):
        return BoxLayoutWidget()


SAPP().run()