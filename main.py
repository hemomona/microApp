# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main.py
# Time       ：2022/4/4 15:32
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7 kivy 2.1
# Description：main class of micro app,
              directory "data" places the files related with users,
              directory "discard" places codes what I test,
              directory "font" is used to replace default font. can not modify config.py of kivy in my ubuntu18,
              directory "pics" places pictures embedded in the app.
"""
import os
import sqlite3
import logging.config
from collections import deque

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from plyer import email, storagepath, uniqueid

from sql import sql_create_table, sql_select_example, sql_insert_example, sql_select_records, sql_disable_arecord, \
    sql_insert_arecord, sql_update_arecord

# replace default font
resource_add_path(os.path.abspath('./font'))
LabelBase.register('Roboto', 'MSYH.TTC')

# basic info here
app_version = '1.0.1'
db_filepath = './records.db'
log_filepath = './logging.log'
# data directory places ID_table.json and ID_picture.json,
# need to place something before package, or it will be excluded.
data_path = './data/'
logging.config.fileConfig('./log.conf')
logger = logging.getLogger('mylog')

# Loading Multiple .kv files
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# MUST LOAD Micro.kv if on ANDROID!!!!!!!!!!!!!
Builder.load_file('Micro.kv')
Builder.load_file('screenkv/records.kv')
Builder.load_file('screenkv/arecord.kv')
Builder.load_file('screenkv/information.kv')
Builder.load_file('screenkv/experiment.kv')


# Declare MainScreen in Micro.kv
class MainScreen(Screen):
    def goto_information(self):
        self.manager.current = 'information'

    def goto_records(self):
        self.manager.current = 'records'

    def goto_feedback(self):
        app_path = storagepath.get_application_dir()
        device_id = uniqueid.get_uid()
        f = open(log_filepath, 'r', encoding='UTF-8')
        log_list = list(deque(f, 30))                   # only save the last 30 lines of log file
        f.close()
        log_info = '\n'
        for item in log_list:
            log_info = log_info + item
        # create_chooser is only supported on Android,
        # if on windows, set it True causes unreadable code.
        email.send(recipient='18146856052@163.com',
                   subject='User Feedback',
                   text='应用版本: ' + app_version + '\n'
                        '保存路径: ' + app_path + '\n'
                        '设备ID: ' + device_id + '\n'
                        '其它: \n\n\n日志信息: ' + log_info,
                   create_chooser=True)


# Declare RecordsScreen in records.kv
class RecordsScreen(Screen):
    check_ref = {}                                      # (id, checkbox instance)
    button_ref = {}                                     # (button instance, id)
    active_record_id = NumericProperty(1)               # id of the pressed button
    sv = ScrollView()

    def __init__(self, **kwargs):
        super(RecordsScreen, self).__init__(**kwargs)
        # if there is no database in the path, it will create one
        conn = sqlite3.connect(db_filepath)
        conn.text_factory = str
        curs = conn.cursor()
        conn.execute(sql_create_table)
        curs.execute(sql_select_example)
        # print(not curs.fetchone())                    # curs.fetchone() is None when fetch nothing
        if not curs.fetchone():
            conn.execute(sql_insert_example)
        conn.commit()
        conn.close()
        Clock.schedule_once(self.show_records)          # call show_records once

    def show_records(self, dt):
        conn = sqlite3.connect(db_filepath)
        conn.text_factory = str
        rows = conn.execute(sql_select_records)
        # layout is GridLayout, layout contains many grids (GridLayout).
        # in a row, left grid contains a checkbox.kv, right grid contains a box
        # a box is vertical and contains a button and a label
        # I AM SO GOOD! refresh the screen through clock, remove and re-add of self.sv.
        self.remove_widget(self.sv)
        self.sv = ScrollView(size_hint=(1, 0.95))
        layout = GridLayout(cols=1, padding='40dp', spacing='10dp', size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for row in rows:
            grid = GridLayout(cols=2, size_hint_y=None, height='50dp')
            c = CheckBox(size_hint_x=None, width='20dp')
            self.check_ref[row[0]] = c                  # Stores a reference to the CheckBox instance
            box = BoxLayout(orientation='vertical')
            b = Button(text=row[1], on_release=self.goto_arecord, font_size='18sp', size_hint_y=None, height='30dp',
                       color=(1, 1, 0, 1), background_color=(0, 0, 0))
            self.button_ref[b] = row[0]                 # Stores a reference to the Button instance
            # italic display bacteria name, regular method and former 10 chars of timestamp
            l = Label(text='[font=timesi]'+row[2] + '[/font] ' + row[3] + ' ' + row[4] + ' ' + row[5][:10],
                      markup=True, font_size='14sp', size_hint_y=None, height='20dp', color=(1, 1, 1, 0.5))
            box.add_widget(b)
            box.add_widget(l)
            grid.add_widget(c)
            grid.add_widget(box)
            layout.add_widget(grid)
        self.sv.add_widget(layout)
        self.add_widget(self.sv)
        conn.commit()
        conn.close()

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

    def goto_arecord(self, instance):
        self.active_record_id = int(self.button_ref.get(instance))
        self.manager.get_screen('arecord').record_id = self.active_record_id
        self.manager.current = 'arecord'


# Declare ARecordScreen in arecord.kv
class ARecordScreen(Screen):
    record_id = NumericProperty(1)                      # comes from RecordsScreen.active_record_id

    # bind it to the active_record_id in Micro.kv, just for showing on_ attribute of Kivy
    # Now this function is useless
    def on_record_id(self, widget, records):
        pass

    def goto_records(self):
        self.manager.current = 'records'

    def save_arecord(self):
        print('have not implemented')


# Declare InformationScreen in information.kv
class InformationScreen(Screen):
    subject = ObjectProperty()
    object = ObjectProperty()
    researcher = ObjectProperty()
    method = ObjectProperty()
    insert_record_id = NumericProperty(1)

    def vali_subject(self):
        strs = self.subject.text
        if len(strs) > 20:
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.4, 0.2), content=Label(text='输入名称过长！'))
            popup.open()
            self.subject.text = ''
            return False
        return True

    def vali_object(self):
        strs = self.object.text
        # allow space, dot, (, ) in the object
        strs = strs.replace('.', '').replace(' ', '').replace('(', '').replace(')', '')
        # Chinese char will be directly judged as True by isalpha()
        if not strs.encode('utf-8').isalpha():
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.4, 0.2), content=Label(text='包含非法字符！'))
            popup.open()
            self.object.text = ''
            return False
        return True

    def start_record(self):
        if self.subject.text == '' or self.object.text == '' or self.researcher.text == '':
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.4, 0.2), content=Label(text='包含空字符串！'))
            popup.open()
        elif self.method.text not in self.method.values:
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.4, 0.2), content=Label(text='未选实验方法！'))
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
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.4, 0.2), content=Label(text='预期外的错误！'))
            popup.open()

    def goto_main(self):
        self.manager.current = 'main'

    def goto_experiment(self):
        self.manager.get_screen('experiment').record_id = self.insert_record_id
        self.manager.current = 'experiment'


# Declare ExperimentScreen in experiment.kv
class ExperimentScreen(Screen):
    record_id = NumericProperty(1)                      # comes from InformationScreen.insert_record_id
    purpose = ObjectProperty()
    principle = ObjectProperty()
    equipment = ObjectProperty()
    steps = ObjectProperty()
    result = ObjectProperty()
    discussion = ObjectProperty()
    lo = BoxLayout()                                    # BoxLayout in ScrollView
    bb = Bubble()                                       # Bubble usually is hidden
    pt = Popup()                                        # Popup of table-create
    pc = Popup()                                        # Popup of chart-create
    spt = ObjectProperty()                              # Spinner of table-create popup
    spc = ObjectProperty()                              # Spinner of chart-create popup
    table_title = ObjectProperty()
    chart_title = ObjectProperty()
    table_rows = ObjectProperty()
    table_cols = ObjectProperty()
    tables = {}                                         # (title-section, table instance)

    def __init__(self, **kwargs):
        super(ExperimentScreen, self).__init__(**kwargs)
        self.remove_widget(self.bb)
        self.remove_widget(self.pt)
        self.remove_widget(self.pc)

    def show_bubble(self):
        if self.bb in self.children:
            self.remove_widget(self.bb)
        else:
            self.add_widget(self.bb)

    def show_table_popup(self):
        if self.pt in self.children:
            self.remove_widget(self.pt)
        else:
            self.remove_widget(self.bb)
            self.add_widget(self.pt)

    def show_chart_popup(self):
        if self.pc in self.children:
            self.remove_widget(self.pc)
        else:
            self.remove_widget(self.bb)
            self.add_widget(self.pc)

    def save_arecord(self):
        self.save_tables()
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        curs.execute(sql_update_arecord, (self.purpose.text, self.principle.text, self.equipment.text,
                                          self.steps.text, self.result.text, self.discussion.text, self.record_id))
        conn.commit()
        conn.close()
        Clock.schedule_once(self.manager.get_screen('records').show_records)
        Popup(title='~ information ~', title_align='center', size_hint=(0.4, 0.2), content=Label(text='保存成功')).open()

    def add_table(self):
        table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
        if self.sp.text not in self.sp.values:
            self.sp.is_open = True
        elif table_store.exists(self.table_title.text):
            self.table_title.text = '此表格已存在！'
        elif not self.table_rows.text.isdigit():
            self.table_rows.text = ''
        elif not self.table_cols.text.isdigit():
            self.table_cols.text = ''
        else:
            title = self.table_title.text
            rownum = int(self.table_rows.text)
            colnum = int(self.table_cols.text)
            table = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(20*rownum+30))
            table.add_widget(Label(text=title + '-' + self.sp.text))
            for r in range(rownum):
                row = GridLayout(cols=colnum)
                for c in range(int(colnum)):
                    row.add_widget(TextInput(font_size='12sp'))
                table.add_widget(row)
            self.tables[title+'-'+self.sp.text] = table
            self.lo.add_widget(table)
            self.table_title.text = ''
            self.table_rows.text = ''
            self.table_cols.text = ''
            self.remove_widget(self.pt)

    def save_tables(self):
        table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
        # forget items() will cause ValueError: too many values to unpack (expected 2)
        for k, v in self.tables.items():                # access every table
            # !!!!!!!the data in a table is reversed AND reverse() returns None!!!!!!!
            l = []
            i = k.rfind('-')
            for r in v.children:                        # access every row
                for ti in r.children:                   # access every cell
                    l.append(ti.text)
            l.reverse()
            table_store.put(k[:i], data=l, section=k[i+1:])

    def add_chart(self):
        print('todo')

    def goto_main(self):
        self.manager.current = 'main'


class MicroApp(App):
    def build(self):
        # Kivy supports only 1 window per application
        # my HUAWEI mate 40E size is (1080, 2264)
        Window.size = (360, 720)
        self.title = 'micro-GCFP'
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(RecordsScreen(name='records'))
        sm.add_widget(ARecordScreen(name='arecord'))
        sm.add_widget(InformationScreen(name='information'))
        sm.add_widget(ExperimentScreen(name='experiment'))
        return ExperimentScreen()


if __name__ == '__main__':
    # The name of the kv file must match the part before the App ending.
    # e.g. pongApp -> pong.kv
    try:
        MicroApp().run()
    except Exception as e:
        logger.exception(e)
