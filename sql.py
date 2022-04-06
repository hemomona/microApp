# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : sql.py
# Time       ：2022/4/6 16:02
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：all the used sql
"""
# ID, if delete, record subject, bacteria name, experiment method...
sql_create_record = '''create table if not exists record
                       (ID integer primary key autoincrement,
                        enable boolean default 1,
                        subject text not null,
                        bacteria text not null,
                        method text not null,
                        researcher text not null,
                        create_time TimeStamp default (datetime('now','localtime')),
                        modify_time TimeStamp default (datetime('now','localtime')),
                        objective text)'''

sql_insert_record = '''insert into record(enable, subject, bacteria, method, researcher, objective) values
                       (1, '生长曲线实验示例', 'E. coli', '比浊法', '来自豆丁网示例', '1.练习无菌操作技术，学习液体培养基配制和接种方法；\n
                        2.掌握利用细菌悬液浑浊度间接测定细菌生长的方法；\n3.了解细菌生长曲线特征，测定细菌繁殖代时；') '''

sql_select_example = '''select * from record where ID = 1'''

sql_select_records = '''select ID, subject, bacteria, method, researcher, create_time from record where enable = 1'''

sql_disable_record = '''update record set enable = 0 where ID = ?'''
