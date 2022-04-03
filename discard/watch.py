#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 15:26
# @Author  : Jago
# @Email   : 18146856052@163.com
# @File    : watch.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from time import time
from kivy.core.window import Window
from kivy.properties import StringProperty
from functools import partial
from kivy.lang import Builder

Builder.load_string('''
<myWatch>
    BoxLayout:
        orientation: 'vertical'
        spacing:15
        padding:38
        BoxLayout:
            Label:
                color: 1,0,0,1
                font_size: '30sp'
                text:root.mode_label
        BoxLayout:
            orientation: 'horizontal'
            Label:
                id: hour
                font_size: '40sp'
                text:root.hour
            Label:
                font_size: '40sp'
                text:':'
            Label:
                id: min
                font_size:'40sp'
                text:root.min
            Label:
                font_size:'40sp'
                text:':'
            Label:
                id:sec
                font_size:'40sp'
                text:root.sec
            Label:
                font_size:'40sp'
                text:':'
            Label:
                id:csec
                font_size:'40sp'
                text:root.csec
        BoxLayout:   
            Label:
                font_size: '15sp'
                text:'hour'
                pos_hint: {"center_x": .5, "center_y": .9}
            Label:
                font_size: '15sp'
                text:':'
                pos_hint: {"center_x": .5, "center_y": .9}

            Label:
                font_size:'15sp'
                text:'min'
                pos_hint: {"center_x": .5, "center_y": .9}
            Label:
                font_size:'15sp'
                text:':'
                pos_hint: {"center_x": .5, "center_y": .9}
            Label:
                font_size:'15sp'
                text:'sec'
                pos_hint: {"center_x": .5, "center_y": .9}
            Label:
                font_size:'15sp'
                text:':'
                pos_hint: {"center_x": .5, "center_y": .9}
            Label:
                font_size:'15sp'
                text:'csec'
                pos_hint: {"center_x": .5, "center_y": .9}
          
        BoxLayout:
            orientation: 'vertical'
            Label
                font_size: '24sp'
                text:'Timer Input Area'
            Label:
                id:message
                font_size: '20sp'
                color: 1,0,0,1
                text:root.message
                pos_hint: {"center_x": .5, "center_y": .9}
                                
        BoxLayout:
            orientation: 'horizontal'
            spacing:280

            TextInput:
                id:hour_input
                multiline: True
                readonly: False
                halign:'center'
                font_size:'55'
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.1, .6)
                
            TextInput:
                id:min_input
                multiline: True
                readonly: False
                halign:'center'
                font_size:'55'
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.1, .6)
                
            TextInput:
                id:sec_input
                multiline: True
                readonly: False
                halign:'center'
                font_size:'55'
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.1, .6)

        BoxLayout:
            orientation: 'horizontal'
            Label:
                font_size: '15sp'
                text:'hour'
                pos_hint: {"center_x": .5, "center_y": .9}
            Label:
                font_size: '15sp'
                text:':'
                pos_hint: {"center_x": .5, "center_y": .9}

            Label:
                font_size:'15sp'
                text:'min'
                pos_hint: {"center_x": .5, "center_y": .9}
            Label:
                font_size:'15sp'
                text:':'
                pos_hint: {"center_x": .5, "center_y": .9}
            Label:
                font_size:'15sp'
                text:'sec'
                pos_hint: {"center_x": .5, "center_y": .9}

        BoxLayout:
            orientation: 'horizontal'
            spacing:60
            Button:
                font_size:'20sp'
                text:'Stopwatch Mode'
                pos_hint: {"center_x": .8, "center_y": .8}
                size_hint: (.8, .8)
                on_press:root.stopwatch_mode()
            Button:
                font_size:'20sp'
                text:'Timer Mode'
                pos_hint: {"center_x": .8, "center_y": .8}
                size_hint: (.8, .8)
                on_press:root.timer_mode()
                            
        BoxLayout:
            orientation: 'horizontal'
            spacing:80
            Button:
                id:start
                font_size:'24sp'
                text:'start'
                on_press:root.start()
            Button:
                id:stop
                font_size:'24sp'
                text:'stop'
                on_press:root.stop()
            Button:
                id:reset
                font_size:'24sp'
                text:'reset'
                on_press:root.reset()          
''')


class myWatch(BoxLayout):
    hour = StringProperty()
    min = StringProperty()
    sec = StringProperty()
    csec = StringProperty()
    mode_label = StringProperty()
    message = StringProperty()

    def __init__(self, **kwargs):
        super(myWatch, self).__init__(**kwargs)
        self.reset()

    def setTime(self, current_time, key):
        self.all_interval = time() - current_time
        self.interval = time() - current_time
        if self.start_flag:
            self.all_interval += self.escpted
        if self.mode == 'Stopwatch' and self.stop_flag:
            self.interval += self.escpted  # 如果暂停过则需加上已经经过的时间
        elif self.mode == 'Timer':
            self.interval = abs(time() - self.stop_time)  # 计时器的时间间隔区别于秒表的时间间隔
            if self.start_flag:
                self.interval -= self.escpted

        hours = int(self.interval / 60 / 60)
        mins = int((self.interval - hours * 60 * 60) / 60)
        seconds = int(self.interval - hours * 60 * 60 - mins * 60)
        cseconds = int((self.interval - hours * 60 * 60 - mins * 60 - seconds) * 100)
        self.ids['hour'].text = '{:0>2d}'.format(hours)  # 小于2位则补0
        self.ids['min'].text = '{:0>2d}'.format(mins)
        self.ids['sec'].text = '{:0>2d}'.format(seconds)
        self.ids['csec'].text = '{}'.format(cseconds)

        # 处于定时器模式且剩余时间小于0.3秒则复位
        if self.mode == 'Timer' and self.interval < 0.3:
            self.reset()
            self.ids['message'].text = 'Time Up'

    def timer_mode(self):
        self.reset()
        self.mode = 'Timer'
        self.mode_label = 'Timer Mode'

    def stopwatch_mode(self):
        self.reset()
        self.mode = 'Stopwatch'
        self.mode_label = 'Stopwatch Mode'

    def start(self):
        if not self.mode:
            self.mode_label = 'please choose a mode'
        else:
            # 防止多次开始
            if not self.start_flag:
                self.start_time = time()
                if self.mode == 'Timer':
                    try:
                        # 计算用户输入的时间，单位秒
                        input_time = int(self.ids['hour_input'].text) * 60 * 60 + \
                                     int(self.ids['min_input'].text) * 60 + int(self.ids['sec_input'].text)
                        self.stop_time = self.start_time + input_time  # 计时器的停止时间
                        self.ids['message'].text = ''
                    except:
                        self.ids['message'].text = 'Please enter the correct number'
                        return

                    if self.stop_flag:  # 如果暂停过，则需减去经过的时间
                        self.stop_time -= self.escpted
                self.start_flag = True
                self.event = Clock.schedule_interval(partial(self.setTime, self.start_time), 0.1)

    def stop(self, reset_flag=False):
        if self.mode:
            self.event.cancel()
            self.start_flag = False  # 停止过后再按开始才有效
            if not reset_flag:
                self.stop_flag = True

                self.escpted = self.all_interval

    def reset(self):
        try:
            self.stop(reset_flag=True)
        except:
            pass
        self.ids['hour'].text = '00'
        self.ids['min'].text = '00'
        self.ids['sec'].text = '00'
        self.ids['csec'].text = '00'
        self.ids['hour_input'].text = '00'
        self.ids['min_input'].text = '00'
        self.ids['sec_input'].text = '00'
        self.mode = ''  # 用来记录当前模式
        self.mode_label = 'please choose a mode'  # 用于显示模式
        self.start_flag = None  # 用来记录是否可以开始
        self.stop_flag = None  # 用来记录是否暂停过
        self.escpted = 0.  # 用来记录已经经过的时间
        self.ids['message'].text = ''  # 用来进行用户提示


class myWatchApp(App):
    def build(self):
        self.title = 'My Watch'

        return myWatch()


if __name__ == '__main__':
    app = myWatchApp()
    app.run()
