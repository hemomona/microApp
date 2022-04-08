# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main.py
# Time       ：2022/4/4 15:32
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7 kivy 2.1
# Description：main class of micro app,
              directory "discard" places codes what I test,
              directory "fonts" is used to replace default font on my windows11,
              but not used on Android for having modified config.py of kivy in my ubuntu18.
"""
import os
import sqlite3
import logging.config
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
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
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from plyer import email, storagepath, uniqueid

from sql import sql_create_table, sql_select_example, sql_insert_example, sql_select_records, sql_disable_arecord, \
    sql_insert_arecord, sql_update_arecord

# replace default font on my Windows computer
# if on Android phone, need to be deleted the following 2 lines while packaging
resource_add_path(os.path.abspath('./font'))
LabelBase.register('Roboto', 'MSYH.TTC')

# basic info here
app_version = '1.0.1'
db_filepath = 'records.db'
# logging.config.fileConfig('log.conf')
# logger = logging.getLogger('mylog')

# Loading Multiple .kv files
# Builder.load_file('screenkv/feedback.kv')
Builder.load_file('screenkv/records.kv')
Builder.load_file('screenkv/arecord.kv')
Builder.load_file('screenkv/information.kv')
Builder.load_file('screenkv/experiment.kv')


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


# Declare RecordsScreen in kv
class RecordsScreen(Screen):
    # (id, checkbox instance)
    check_ref = {}
    # (button instance, id)
    button_ref = {}
    # id of the pressed button
    active_record_id = NumericProperty(1)
    sv = ScrollView()

    def __init__(self, **kwargs):
        super(RecordsScreen, self).__init__(**kwargs)
        # if there is no database in the path, it will create one
        conn = sqlite3.connect(db_filepath)
        conn.text_factory = str
        curs = conn.cursor()
        conn.execute(sql_create_table)
        curs.execute(sql_select_example)
        # print(not curs.fetchone()) # so curs.fetchone() is None when fetch nothing
        if not curs.fetchone():
            conn.execute(sql_insert_example)
        conn.commit()
        conn.close()
        Clock.schedule_once(self.show_records)

    def show_records(self, dt):
        conn = sqlite3.connect(db_filepath)
        conn.text_factory = str
        rows = conn.execute(sql_select_records)
        # layout is scrollview, layout contains many grids.
        # in a row, left grid contains a checkbox.kv, right grid contains a box
        # a box is vertical and contains a button and a label
        # I AM SO GOOD! refresh the screen through clock, remove and re-add of self.sv.
        self.remove_widget(self.sv)
        self.sv = ScrollView(size_hint=(1, 0.95))
        layout = GridLayout(cols=1, padding=40, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for row in rows:
            grid = GridLayout(cols=2, size_hint_y=None, height=50)
            c = CheckBox(size_hint_x=None, width=20)
            # Stores a reference to the CheckBox instance
            self.check_ref[row[0]] = c
            box = BoxLayout(orientation='vertical')
            b = Button(text=row[1], on_release=self.show_arecord, font_size='18sp', size_hint_y=None, height=30,
                       color=(1, 1, 0, 1), background_color=(0, 0, 0))
            self.button_ref[b] = row[0]
            # italic display bacteria name, regular method and former 10 chars of timestamp
            l = Label(text=row[2] + ' ' + row[3] + ' ' + row[4] + ' ' + row[5][:10],
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

    def show_arecord(self, instance):
        self.active_record_id = int(self.button_ref.get(instance))
        self.goto_arecord()

    def dele_records(self):
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        # Iterate over the dictionary storing the CheckBox widgets
        for idx, wgt in self.check_ref.items():
            if wgt.active:
                curs.execute(sql_disable_arecord, (idx, ))
        conn.commit()
        conn.close()
        Clock.schedule_once(self.show_records)

    def goto_main(self):
        self.manager.current = 'main'

    def goto_arecord(self):
        self.manager.current = 'arecord'


# Declare ARecordScreen in kv
class ARecordScreen(Screen):
    record_id = NumericProperty(1)

    # bind it to the active_record_id in Micro.kv, just for showing on_ attribute of Kivy
    def on_record_id(self, widget, records):
        # print(self.record_id)
        pass

    def goto_records(self):
        self.manager.current = 'records'

    def save_arecord(self):
        print('have not implemented')


# Declare InformationScreen in kv
class InformationScreen(Screen):
    subject = ObjectProperty()
    object = ObjectProperty()
    researcher = ObjectProperty()
    method = ObjectProperty()
    insert_record_id = NumericProperty(1)

    def vali_subject(self):
        strs = self.subject.text
        if len(strs) > 20:
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.5, 0.2),
                          content=Label(text='输入名称过长！'))
            popup.open()
            self.subject.text = ''
            return False
        return True

    def vali_object(self):
        strs = self.object.text
        # allow space, dot, (, ) in the object
        strs = strs.replace('.', '').replace(' ', '').replace('(', '').replace(')', '')
        # Chinese char will be judged as True by isalpha()
        if not strs.encode('utf-8').isalpha():
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.5, 0.2), content=Label(text='包含非法字符！'))
            popup.open()
            self.object.text = ''
            return False
        return True

    def start_record(self):
        if self.subject.text == '' or self.object.text == '' or self.researcher.text == '':
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.5, 0.2), content=Label(text='包含空字符串！'))
            popup.open()
        elif self.method.text not in self.method.values:
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.5, 0.2), content=Label(text='未选实验方法！'))
            popup.open()
        elif self.vali_subject() and self.vali_object():
            conn = sqlite3.connect(db_filepath)
            conn.text_factory = str
            curs = conn.cursor()
            curs.execute(sql_insert_arecord, (self.subject.text, self.object.text, self.method.text, self.researcher.text))
            self.insert_record_id = curs.lastrowid
            conn.commit()
            conn.close()
            self.goto_experiment()
        else:
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.5, 0.2),
                          content=Label(text='预期外的错误！'))
            popup.open()

    def goto_main(self):
        self.manager.current = 'main'

    def goto_experiment(self):
        self.manager.current = 'experiment'


# Declare ExperimentScreen in kv
class ExperimentScreen(Screen):
    record_id = NumericProperty(1)
    purpose = StringProperty('')
    principle = StringProperty('')
    equipment = StringProperty('')
    step = StringProperty('')
    result = StringProperty('')
    discussion = StringProperty('')
    sv = ScrollView()

    def __init__(self, **kwargs):
        super(ExperimentScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.refresh_content)

    def refresh_content(self, dt):
        self.remove_widget(self.sv)
        self.sv = ScrollView(size_hint=(1, 0.95))
        layout = BoxLayout(orientation='vertical', padding=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        layout.add_widget(Label(text='目的', font_size='16sp', size_hint=(0.1, None), height=30, pos_hint={'right': 0.2}))
        layout.add_widget(TextInput(text=self.purpose, size_hint_y=None, height=120))
        layout.add_widget(Label(text='原理', font_size='16sp', size_hint=(0.1, None), height=30, pos_hint={'right': 0.2}))
        layout.add_widget(TextInput(text=self.principle, size_hint_y=None, height=240))
        layout.add_widget(Label(text='材料', font_size='16sp', size_hint=(0.1, None), height=30, pos_hint={'right': 0.2}))
        layout.add_widget(TextInput(text=self.equipment, size_hint_y=None, height=80))
        layout.add_widget(Label(text='步骤', font_size='16sp', size_hint=(0.1, None), height=30, pos_hint={'right': 0.2}))
        layout.add_widget(TextInput(text=self.step, size_hint_y=None, height=360))
        layout.add_widget(Label(text='结果', font_size='16sp', size_hint=(0.1, None), height=30, pos_hint={'right': 0.2}))
        layout.add_widget(TextInput(text=self.result, size_hint_y=None, height=300))
        layout.add_widget(Label(text='讨论', font_size='16sp', size_hint=(0.1, None), height=30, pos_hint={'right': 0.2}))
        layout.add_widget(TextInput(text=self.discussion, size_hint_y=None, height=240))
        self.sv.add_widget(layout)
        self.add_widget(self.sv)

    def goto_main(self):
        self.manager.current = 'main'

    def save_arecord(self):
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        curs.execute(sql_update_arecord, (datetime.now(), self.purpose, self.principle, self.equipment,
                                          self.step, self.result, self.discussion, self.record_id))
        conn.commit()
        conn.close()
        self.manager.current = 'records'


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
    # try:
    MicroApp().run()
    # except Exception as e:
    #     logger.exception(e)
