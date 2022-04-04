# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main.py
# Time       ：2022/4/4 15:32
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


# Loading Multiple .kv files
Builder.load_file('screens/feedback.kv')
Builder.load_file('screens/records.kv')
Builder.load_file('screens/experiment.kv')


# Declare MainScreen in kv
class MainScreen(Screen):
    pass


# Declare FeedbackScreen in kv
class FeedbackScreen(Screen):
    pass


# Declare RecordsScreen in kv
class RecordsScreen(Screen):
    pass


# Declare ExperimentScreen in kv
class ExperimentScreen(Screen):
    pass


# Declare MyScreenManager in kv
class MyScreenManager(ScreenManager):
    pass


class MicroApp(App):
    def build(self):
        # Kivy supports only 1 window per application
        Window.size = (360, 792)
        return


if __name__ == '__main__':
    # The name of the kv file must match the part before the App ending.
    # e.g. pongApp -> pong.kv
    MicroApp().run()
