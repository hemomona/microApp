# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : checkbox.kv.py
# Time       ：2022/4/6 15:10
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class CheckBoxBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(CheckBoxBoxLayout, self).__init__(**kwargs)

        # 通过ID获取到checkbox部件并绑定方法
        self.ids.first_check_0.bind(active=self.on_checkbox_active)
        self.ids.first_check_1.bind(active=self.on_checkbox_active)
        self.ids.first_check_2.bind(active=self.on_checkbox_active)
        self.ids.first_check_3.bind(active=self.on_checkbox_active)

    @staticmethod
    def on_checkbox_active(checkbox, value):
        if value:  # 这里意是如果checkbox传过来的value为True时，打印下面的内容
            print('这个选择框', checkbox, '被选中', value)
        else:
            print('这个选择框', checkbox, '没有选中', value)


class CheckBoxApp(App):
    def build(self):
        return CheckBoxBoxLayout()


if __name__ == '__main__':
    CheckBoxApp().run()