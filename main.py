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
              table_store.put(k, data=l, row=v[1], col=v[2], section=v[3])
              chart_store.put(k, path=v[1], section=v[2])
"""
import os
import re
import sqlite3
import logging.config
from collections import deque

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from scipy import interpolate

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty
from kivy.resources import resource_add_path
from kivy.core.image import Image
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
    sql_insert_arecord, sql_update_arecord, sql_select_arecord

# replace default font of kivy to display Chinese
resource_add_path(os.path.abspath('./font'))
LabelBase.register('Roboto', 'MSYH.TTC')

# replace default font of matplotlib to display Chinese
mpl.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('ggplot')

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
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.4, 0.2),
                          content=Label(text='包含空字符串！'))
            popup.open()
        elif self.method.text not in self.method.values:
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.4, 0.2),
                          content=Label(text='未选实验方法！'))
            popup.open()
        elif self.vali_subject() and self.vali_object():
            conn = sqlite3.connect(db_filepath)
            conn.text_factory = str
            curs = conn.cursor()
            curs.execute(sql_insert_arecord,
                         (self.subject.text, self.object.text, self.method.text, self.researcher.text))
            self.insert_record_id = curs.lastrowid
            conn.commit()
            conn.close()
            self.goto_experiment()
        else:
            popup = Popup(title='× error ×', title_align='center', size_hint=(0.4, 0.2),
                          content=Label(text='预期外的错误！'))
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
    pd = Popup()                                        # Popup of delete widget
    spt = ObjectProperty()                              # Spinner of table-create popup
    spc = ObjectProperty()                              # Spinner of data reference in chart-create popup
    spdt = ObjectProperty()                             # Spinner of delete table popup
    spdc = ObjectProperty()                             # Spinner of delete chart popup
    spcs = ObjectProperty()                             # Spinner of section in chart-create popup
    spci = ObjectProperty()                             # Spinner of interpolation in chart-create popup
    table_title = ObjectProperty()
    table_rows = ObjectProperty()
    table_cols = ObjectProperty()
    # in the _table.json storage, it is title: {data, row, col, section}
    tables = {}                                         # (title, [table instance, row, col, section])
    chart_title = ObjectProperty()
    chart_rows = ObjectProperty()
    chart_cols = ObjectProperty()
    chart_xaxis = ObjectProperty()
    chart_xlabel = ObjectProperty()
    chart_ylabel = ObjectProperty()
    # in the _chart.json storage, it is title: {path, section}
    charts = {}                                         # (title, [chart instance, filepath, section])

    def __init__(self, **kwargs):
        super(ExperimentScreen, self).__init__(**kwargs)
        self.remove_widget(self.bb)
        self.remove_widget(self.pt)
        self.remove_widget(self.pc)
        self.remove_widget(self.pd)

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
            # table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
            # self.spc.values = table_store.keys()
            self.spc.values = self.tables.keys()
            self.remove_widget(self.bb)
            self.add_widget(self.pc)

    def show_dele_popup(self):
        if self.pd in self.children:
            self.remove_widget(self.pd)
        else:
            self.spdt.values = self.tables.keys()
            self.spdc.values = self.charts.keys()
            self.remove_widget(self.bb)
            self.add_widget(self.pd)

    def save_arecord(self):
        self.save_tables()
        self.save_charts()
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        curs.execute(sql_update_arecord, (self.purpose.text, self.principle.text, self.equipment.text,
                                          self.steps.text, self.result.text, self.discussion.text, self.record_id))
        conn.commit()
        conn.close()
        # Clock.schedule_once(self.manager.get_screen('records').show_records)
        Popup(title='~ information ~', title_align='center', size_hint=(0.4, 0.2),
              content=Label(text='保存成功！')).open()

    def add_table(self):
        table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
        if self.spt.text not in self.spt.values:
            self.spt.is_open = True
        elif table_store.exists(self.table_title.text):
            Popup(title='× error ×', title_align='center', size_hint=(0.6, 0.2),
                  content=Label(text='此表格已存在！')).open()
            self.table_title.text = ''
        elif not self.table_rows.text.isdigit():
            self.table_rows.text = ''
        elif not self.table_cols.text.isdigit():
            self.table_cols.text = ''
        else:
            title = self.table_title.text
            rownum = int(self.table_rows.text)
            colnum = int(self.table_cols.text)
            table = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(20*rownum+30))
            table.add_widget(Label(text=title + '-' + self.spt.text))
            for r in range(rownum):
                row = GridLayout(cols=colnum)
                for c in range(int(colnum)):
                    row.add_widget(TextInput(font_size='12sp', multiline=False))
                table.add_widget(row)
            self.tables[title] = [table, rownum, colnum, self.spt.text]
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
            # i = k.rfind('-')
            for r in v[0].children:                     # access every row
                for ti in r.children:                   # access every cell
                    l.append(ti.text)
            l.reverse()
            table_store.put(k, data=l, row=v[1], col=v[2], section=v[3])

    def add_chart(self):
        chart_store = JsonStore(data_path + str(self.record_id) + '_chart.json')
        if not self.spc.values:                         # spc.values is False when it contains nothing
            Popup(title='× error ×', title_align='center', size_hint=(0.6, 0.2),
                  content=Label(text='需要先行添加表格并且保存！')).open()
            self.remove_widget(self.pc)
        elif self.spc.text not in self.spc.values:
            self.spc.is_open = True
        elif self.spcs.text not in self.spcs.values:
            self.spcs.is_open = True
        elif self.spci.text not in self.spci.values:
            self.spci.is_open = True
        elif chart_store.exists(self.chart_title.text):
            Popup(title='× error ×', title_align='center', size_hint=(0.6, 0.2),
                  content=Label(text='此图片已存在！')).open()
            self.table_title.text = ''
        elif self.chart_rows.text and self.chart_cols.text:
            Popup(title='× error ×', title_align='center', size_hint=(0.6, 0.2),
                  content=Label(text='不支持同时输入行号和列号！')).open()
            self.chart_rows.text = ''
            self.chart_cols.text = ''
        else:
            table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
            table = table_store.get(self.spc.text)
            table_data = table['data']
            table_row = table['row']
            table_col = table['col']
            title = self.chart_title.text
            x = []
            y = []
            ll = []                                       # legend labels
            illegal = False                               # if the data is illegal
            illegal_reason = ''
            if self.chart_rows.text:                      # access rows
                if self.chart_xaxis.text:                 # access the x values user inputed
                    xaxis = re.sub('[^0-9^,.]', '', self.chart_xaxis.text)       # only save number, ,, ..
                    xaxl = xaxis.split(',')
                    if len(xaxl) != table_col - 1:        # -1 because of excluding 1st col
                        illegal = True
                        illegal_reason = 'x值个数错误！'
                    else:
                        for xa in xaxl:
                            try:
                                x.append(float(xa))
                            except ValueError:
                                illegal = True
                                illegal_reason = 'x值包含非数字内容！'
                                break
                else:
                    for i in range(1, table_col):         # +1 because of excluding 1st col
                        try:
                            x.append(float(table_data[i]))
                        except ValueError:
                            illegal = True
                            illegal_reason = '默认x值包含非数字内容！'
                            break

                if not illegal:
                    rows = self.chart_rows.text
                    rows = re.sub('[^0-9^,]', '', rows)    # only save number, ,.
                    for row in rows.split(','):
                        r = int(row)
                        if r > table_row:
                            illegal = True
                            illegal_reason = row + '超出最大行数！'
                            break
                        l = []
                        for i in range(table_col*(r-1)+1, table_col*r):    # +1 because of excluding 1st col
                            try:
                                l.append(float(table_data[i]))
                            except ValueError:
                                illegal = True
                                illegal_reason = row + '行单元格包含非数字内容！'
                                break
                        if illegal:
                            break
                        y.append(l)
                        ll.append(row)
            else:                                           # access cols
                if self.chart_xaxis.text:
                    xaxis = re.sub('[^0-9^,.]', '', self.chart_xaxis.text)       # only save number, ,, ..
                    xaxl = xaxis.split(',')
                    if len(xaxl) != table_row - 1:          # -1 because of excluding 1st row
                        illegal = True
                        illegal_reason = 'x值个数错误！'
                    else:
                        for xa in xaxl:
                            try:
                                x.append(float(xa))
                            except ValueError:
                                illegal = True
                                illegal_reason = 'x值包含非数字内容！'
                                break
                else:
                    # +table_col at 1st place of range because of excluding 1st row
                    for i in range(table_col, table_row*table_col, table_col):
                        try:
                            x.append(float(table_data[i]))
                        except ValueError:
                            illegal = True
                            illegal_reason = '默认x值包含非数字内容！'
                            break

                if not illegal:
                    cols = self.chart_cols.text
                    cols = re.sub('[^0-9^,]', '', cols)
                    for col in cols.split(','):
                        c = int(col)
                        if c > table_col:
                            illegal = True
                            illegal_reason = col + '超出最大列数！'
                            break
                        l = []
                        # +table_col at 1st place of range because of excluding 1st row
                        for i in range(c-1+table_col, table_row*table_col+c-1, table_col):
                            try:
                                l.append(float(table_data[i]))
                            except ValueError:
                                illegal = True
                                illegal_reason = col + '列单元格包含非数字内容！'
                                break
                        if illegal:
                            break
                        y.append(l)
                        ll.append(col)

            if illegal:
                Popup(title='× error ×', title_align='center', size_hint=(0.6, 0.2),
                      content=Label(text=illegal_reason)).open()
            else:
                plt.figure()
                plt.title(title)
                plt.xlabel(self.chart_xlabel.text)
                plt.ylabel(self.chart_ylabel.text)
                x = np.array(x)
                x_smooth = np.linspace(x.min(), x.max(), 300)
                for ay in y:
                    ay = np.array(ay)
                    ay_smooth = interpolate.interp1d(x, ay, kind=self.spci.text)(x_smooth)
                    plt.plot(x_smooth, ay_smooth)
                plt.legend(ll)
                imgpath = data_path + str(self.record_id) + '_' + title + '.png'
                plt.savefig(imgpath)
                chart = BoxLayout(orientation='vertical')
                chart.add_widget(Label(text=title + '-' + self.spcs.text))
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! BUG here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                chart.add_widget(Image(source=imgpath, allow_stretch=True, size_hint=(None, None), size=('360dp', '240dp')))
                self.charts[title] = [chart, imgpath, self.spcs.text]
                self.lo.add_widget(chart)
                self.remove_widget(self.pc)

    def save_charts(self):
        chart_store = JsonStore(data_path + str(self.record_id) + '_chart.json')
        for k, v in self.charts.items():
            chart_store.put(k, path=v[1], section=v[2])

    def dele_widget(self):
        table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
        chart_store = JsonStore(data_path + str(self.record_id) + '_chart.json')
        if self.spdt.text in self.spdt.values:
            removed_table = self.tables.pop(self.spdt.text)
            self.lo.remove_widget(removed_table[0])
            if table_store.exists(self.spdt.text):
                table_store.delete(self.spdt.text)
        if self.spdc.text in self.spdc.values:
            removed_chart = self.charts.pop(self.spdc.text)
            self.lo.remove_widget(removed_chart[0])
            if chart_store.exists(self.spdc.text):
                chart_store.delete(self.spdc.text)
        self.remove_widget(self.pd)

    def goto_main(self):
        self.manager.current = 'main'


# Declare ARecordScreen in arecord.kv
# This can extend from ExperimentScreen. BUT I want to optimize my code
class ARecordScreen(Screen):
    record_id = NumericProperty(1)                      # comes from RecordsScreen.active_record_id
    lo = BoxLayout()                                    # BoxLayout in ScrollView
    bb = Bubble()                                       # Bubble usually is hidden
    pt = Popup()                                        # Popup of table-create
    pc = Popup()                                        # Popup of chart-create
    pd = Popup()                                        # Popup of delete widget
    spt = ObjectProperty()                              # Spinner of table-create popup
    spc = ObjectProperty()                              # Spinner of data reference in chart-create popup
    spdt = ObjectProperty()                             # Spinner of delete table popup
    spdc = ObjectProperty()                             # Spinner of delete chart popup
    spcs = ObjectProperty()                             # Spinner of section in chart-create popup
    spci = ObjectProperty()                             # Spinner of interpolation in chart-create popup
    table_title = ObjectProperty()
    table_rows = ObjectProperty()
    table_cols = ObjectProperty()
    tables = {}                                         # (title, [table instance, row, col, section])
    chart_title = ObjectProperty()
    chart_rows = ObjectProperty()
    chart_cols = ObjectProperty()
    chart_xaxis = ObjectProperty()
    chart_xlabel = ObjectProperty()
    chart_ylabel = ObjectProperty()
    charts = {}                                         # (title, [chart instance, filepath, section])
    sections = ['目的', '原理', '材料', '步骤', '结果', '讨论']

    # bind it to the active_record_id in Micro.kv in last version.
    # Now this function is useless, preserving it for showing on_ attribute of Kivy
    def on_record_id(self, widget, records):
        pass

    def __init__(self, **kwargs):
        super(ARecordScreen, self).__init__(**kwargs)
        self.remove_widget(self.bb)
        self.remove_widget(self.pt)
        self.remove_widget(self.pc)
        self.remove_widget(self.pd)
        Clock.schedule_once(self.show_arecord)

    def show_arecord(self, dt):
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        # cursor parameter should be tuple, or it causes ValueError
        curs.execute(sql_select_arecord, (self.record_id, ))
        record = curs.fetchone()
        for secpart in range(6):
            ti = TextInput(text=record[secpart], halign='left', size_hint_y=None)
            ti.bind(minimum_height=ti.setter('height'))
            self.lo.add_widget(Label(text=self.sections[secpart], size_hint_x=0.1, pos_hint={'right': 0.2}))
            self.lo.add_widget(ti)
            table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
            for k, v in table_store.find(section=self.sections[secpart]):
                self.lo.add_widget(Label(text=k))
                grid = GridLayout(cols=v['col'], size_hint_y=None, height=dp(20*v['row']))
                for d in v['data']:
                    grid.add_widget(TextInput(text=d, font_size='12sp', multiline=False))
                self.lo.add_widget(grid)
                self.tables[k] = [grid, v['row'], v['col'], v['section']]
        conn.commit()
        conn.close()

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
            self.spc.values = self.tables.keys()
            self.remove_widget(self.bb)
            self.add_widget(self.pc)

    def show_dele_popup(self):
        if self.pd in self.children:
            self.remove_widget(self.pd)
        else:
            self.spdt.values = self.tables.keys()
            self.spdc.values = self.charts.keys()
            self.remove_widget(self.bb)
            self.add_widget(self.pd)

    def add_table(self):
        table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
        if self.spt.text not in self.spt.values:
            self.spt.is_open = True
        elif table_store.exists(self.table_title.text):
            Popup(title='× error ×', title_align='center', size_hint=(0.6, 0.2),
                  content=Label(text='此表格已存在！')).open()
            self.table_title.text = ''
        elif not self.table_rows.text.isdigit():
            self.table_rows.text = ''
        elif not self.table_cols.text.isdigit():
            self.table_cols.text = ''
        else:
            title = self.table_title.text
            rownum = int(self.table_rows.text)
            colnum = int(self.table_cols.text)
            self.lo.add_widget(Label(text=title + '-' + self.spt.text))
            table = GridLayout(cols=colnum, size_hint_y=None, height=dp(20*rownum))
            for c in range(rownum*colnum):
                table.add_widget(TextInput(font_size='12sp', multiline=False))
            self.tables[title] = [table, rownum, colnum, self.spt.text]
            self.lo.add_widget(table)
            self.table_title.text = ''
            self.table_rows.text = ''
            self.table_cols.text = ''
            self.remove_widget(self.pt)

    def save_tables(self):
        table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
        for k, v in self.tables.items():                # access every table
            l = []
            for ti in v[0].children:                    # access every cell
                l.append(ti.text)
            l.reverse()
            table_store.put(k, data=l, row=v[1], col=v[2], section=v[3])

    def dele_widget(self):
        table_store = JsonStore(data_path + str(self.record_id) + '_table.json')
        chart_store = JsonStore(data_path + str(self.record_id) + '_chart.json')
        if self.spdt.text in self.spdt.values:
            removed_table = self.tables.pop(self.spdt.text)
            self.lo.remove_widget(removed_table[0])
            if table_store.exists(self.spdt.text):
                table_store.delete(self.spdt.text)
        if self.spdc.text in self.spdc.values:
            removed_chart = self.charts.pop(self.spdc.text)
            self.lo.remove_widget(removed_chart[0])
            if chart_store.exists(self.spdc.text):
                chart_store.delete(self.spdc.text)
        self.remove_widget(self.pd)

    def goto_records(self):
        self.manager.current = 'records'

    def save_arecord(self):
        self.save_tables()
        record = []
        for ti in self.lo.children:
            if isinstance(ti, TextInput):
                record.append(ti.text)
        record.reverse()
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        curs.execute(sql_update_arecord,
                     (record[0], record[1], record[2], record[3], record[4], record[5], self.record_id))
        conn.commit()
        conn.close()
        Popup(title='~ information ~', title_align='center', size_hint=(0.4, 0.2),
              content=Label(text='保存成功！')).open()
        self.lo.clear_widgets()
        Clock.schedule_once(self.show_arecord)


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
