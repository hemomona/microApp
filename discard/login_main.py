#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 15:29
# @Author  : Jago
# @Email   : 18146856052@163.com
# @File    : csdn_main.py
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginScreen(GridLayout):
    # 这里要加super，才能把现有的新初始化方法覆盖掉继承来的旧初始化方法。
    # 另外也要注意，这里调用super的时候没有省略掉**kwargs，这是一种好习惯。
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='中文'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


class MicroApp(App):
    def build(self):
        # return Label(text='Hello world')
        return LoginScreen()


if __name__ == '__main__':
    app = MicroApp()
    app.run()
