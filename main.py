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
from kivy.gesture import GestureDatabase, Gesture
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from plyer import email, storagepath, uniqueid
import sqlite3

# replace default font
import os
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase
resource_add_path(os.path.abspath('./font'))
LabelBase.register('Roboto', 'MSYH.TTC')

app_version = '1.0.1'
db_filepath = 'records.db'

# Loading Multiple .kv files
# Builder.load_file('screenkv/feedback.kv')
Builder.load_file('screenkv/records.kv')
Builder.load_file('screenkv/experiment.kv')


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
                        '设备ID: ' + device_id + '\n\n\n'
                        '其它: \n',
                   create_chooser=True)


# Declare RecordsScreen in kv
class RecordsScreen(Screen):
    def __init__(self, **kwargs):
        super(RecordsScreen, self).__init__(**kwargs)
        # if there is no database in the path, it will create one
        conn = sqlite3.connect(db_filepath)
        conn.text_factory = str
        # ID, if delete, record subject, bacteria name, experiment method...
        sql_create_record = '''create table if not exists record
                               (ID integer primary key autoincrement,
                                enable boolean,
                                subject varchar(20),
                                bacteria text,
                                method text,
                                create_time TimeStamp default (datetime('now','localtime')),
                                modify_time TimeStamp default (datetime('now','localtime')),
                                experiment_path text)'''
        conn.execute(sql_create_record)
        # sql_insert_record = '''insert into record
        #                         (enable, subject, bacteria, method) values
        #                         (1, '生长曲线实验示例', 'E.coli', '比浊法') '''
        # conn.execute(sql_insert_record)
        sql_select_records = '''select ID, subject, bacteria, method, create_time
                                from record where enable = 1'''
        rows = conn.execute(sql_select_records)

        # layout is scrollview, layout contains many grids.
        # in a row, left grid contains a checkbox, right grid contains a box
        # a box is vertical and contains a button and a label
        # sv = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        sv = ScrollView()
        layout = GridLayout(cols=1, padding=40, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for row in rows:
            grid = GridLayout(cols=2, size_hint_y=None, height=50)
            c = CheckBox(color=(0, 1, 1, 1), size_hint_x=None, width=20)
            box = BoxLayout(orientation='vertical')
            b = Button(text=row[1], height=30)
            l = Label(text=row[2]+' '+row[3]+row[4], height=20)
            box.add_widget(b)
            box.add_widget(l)
            # btn = Button(text=str(i), size_hint_y=None, height=40)
            # layout.add_widget(btn)
            grid.add_widget(c)
            grid.add_widget(box)
            layout.add_widget(grid)
        sv.add_widget(layout)
        self.add_widget(sv)
        conn.commit()
        conn.close()

    def goto_main(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

    def dele_record(self, value):
        print(value)


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
