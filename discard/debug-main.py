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
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from plyer import email, storagepath, uniqueid

# from kivy.core.text import LabelBase
# from kivy.resources import resource_add_path
# resource_add_path(os.path.abspath('./font'))
# LabelBase.register('Roboto', 'MSYH.TTC')

Builder.load_file('information-test.kv')
Builder.load_file('BUG.kv')

app_version = '1000'


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


class InformationScreen(Screen):
    pass


class BUGApp(App):
    def build(self):
        msm = ScreenManager()
        msm.add_widget(MainScreen(name='main'))
        msm.add_widget(InformationScreen(name='information'))
        return msm


if __name__ == '__main__':
    BUGApp().run()
