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
import os
import sqlite3

from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.scrollview import ScrollView
from plyer import email, storagepath, uniqueid

from sql import sql_create_record, sql_select_example, sql_insert_record, sql_select_records, sql_disable_record

# replace default font
resource_add_path(os.path.abspath('./font'))
LabelBase.register('Roboto', 'MSYH.TTC')

# basic info here
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
    check_ref = {}
    sv = ScrollView()

    def __init__(self, **kwargs):
        super(RecordsScreen, self).__init__(**kwargs)
        # if there is no database in the path, it will create one
        conn = sqlite3.connect(db_filepath)
        conn.text_factory = str
        curs = conn.cursor()
        conn.execute(sql_create_record)
        curs.execute(sql_select_example)
        # print(not curs.fetchone()) # so curs.fetchone() is None when fetch nothing
        if not curs.fetchone():
            conn.execute(sql_insert_record)
        conn.commit()
        conn.close()
        self.show_records()

    def show_records(self):
        conn = sqlite3.connect(db_filepath)
        conn.text_factory = str
        rows = conn.execute(sql_select_records)
        # layout is scrollview, layout contains many grids.
        # in a row, left grid contains a checkbox.kv, right grid contains a box
        # a box is vertical and contains a button and a label
        layout = GridLayout(cols=1, padding=40, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for row in rows:
            grid = GridLayout(cols=2, size_hint_y=None, height=50)
            c = CheckBox(size_hint_x=None, width=20)
            # Stores a reference to the CheckBox instance
            self.check_ref[row[0]] = c
            box = BoxLayout(orientation='vertical')
            b = Button(text=row[1], font_size='18sp', size_hint_y=None, height=30,
                       color=(1, 1, 0, 1), background_color=(0, 0, 0))
            # italic display bacteria name, regular method and former 10 chars of timestamp
            l = Label(text='[font=timesi]' + row[2] + '[/font] ' + row[3] + ' ' + row[4] + ' ' + row[5][:10],
                      markup=True, font_size='14sp', size_hint_y=None, height=20, color=(1, 1, 1, 0.5))
            box.add_widget(b)
            box.add_widget(l)
            grid.add_widget(c)
            grid.add_widget(box)
            layout.add_widget(grid)
        self.sv.add_widget(layout)
        self.add_widget(self.sv)
        conn.commit()
        conn.close()

    def goto_main(self):
        self.manager.current = 'main'

    def dele_records(self):
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        # Iterate over the dictionary storing the CheckBox widgets
        for idx, wgt in self.check_ref.items():
            if wgt.active:
                curs.execute(sql_disable_record, (idx, ))
        conn.commit()
        conn.close()
        # must execute sql after this transaction committed
        self.remove_widget(self.sv)
        self.sv = ScrollView()
        self.show_records()


# Declare ExperimentScreen in kv
class ExperimentScreen(Screen):
    subject = ObjectProperty()
    object = ObjectProperty()
    researcher = ObjectProperty()
    method = ObjectProperty()

    def vali_subject(self):
        if len(self.subject.text) > 20:
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.5, 0.2),
                          content=Label(text='输入名称过长！'))
            popup.open()
            self.subject.text = ''
            return False
        return True

    def vali_object(self):
        # Chinese char will be judged as True by isalpha()
        if not self.object.text.encode('UTF-8').isalpha():
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.5, 0.2),
                          content=Label(text='包含非法字符！'))
            popup.open()
            self.object.text = ''
            return False
        return True

    def start_record(self):
        if self.subject.text == '' or self.object.text == '' or self.researcher.text == '':
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.5, 0.2),
                          content=Label(text='包含空字符串！'))
            popup.open()
        if self.vali_subject() and self.vali_object() and self.method.text in self.method.values:
            print('yes')

    def goto_main(self):
        self.manager.current = 'main'


class MicroApp(App):
    def build(self):
        # Kivy supports only 1 window per application
        Window.size = (360, 792)
        self.title = 'micro-GCFP'
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(RecordsScreen(name='records'))
        sm.add_widget(ExperimentScreen(name='experiment'))
        return sm


if __name__ == '__main__':
    # The name of the kv file must match the part before the App ending.
    # e.g. pongApp -> pong.kv
    MicroApp().run()
