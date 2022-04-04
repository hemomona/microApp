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
from plyer import email, storagepath, uniqueid

app_version = '1.0.1'

# Loading Multiple .kv files
# Builder.load_file('screens/feedback.kv')
Builder.load_file('screens/records.kv')
Builder.load_file('screens/experiment.kv')


# Declare MainScreen in kv
class MainScreen(Screen):
    def goto_experiment(self):
        self.manager.current = 'experiment'

    def goto_records(self):
        self.manager.current = 'records'

    def goto_feedback(self):
        app_path = storagepath.get_application_dir()
        device_id = uniqueid.get_uid()
        email.send(recipient='18146856052@163.com',
                   subject='app test',
                   text='应用版本: ' + app_version + '\n'
                        '保存路径: ' + app_path + '\n'
                        '设备ID: ' + device_id + '\n'
                        '其它: \n',
                   create_chooser=False)


# Declare FeedbackScreen in kv
# FeedbackScreen has been discarded
# class FeedbackScreen(Screen):
#     pass


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
        self.title = 'micro-GCFP'
        return


if __name__ == '__main__':
    # The name of the kv file must match the part before the App ending.
    # e.g. pongApp -> pong.kv
    MicroApp().run()
