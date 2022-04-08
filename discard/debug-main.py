# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : debug-main.py.py
# Time       ：2022/4/8 21:30
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：debug what cause my app run wrong
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from plyer import email, storagepath, uniqueid

# basic info here
app_version = '1.0.1'


class MainScreen(Screen):
    def goto_information(self):
        self.manager.current = 'information'

    def goto_records(self):
        self.manager.current = 'records'

    def goto_feedback(self):
        app_path = storagepath.get_application_dir()
        device_id = uniqueid.get_uid()
        email.send(recipient='18146856052@163.com',
                   subject='app test',
                   text='应用版本: ' + app_version + '\n'
                        '保存路径: ' + app_path + '\n'
                        '设备ID: ' + device_id + '\n\n\n'
                        '其它: \n',
                   create_chooser=True)


class BUGApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    BUGApp().run()
