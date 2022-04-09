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

'''
id ID, enable 是否可用, subject 报告名称, object 对象名称, method 实验方法,
researcher 实验人员, create_time 创建时间, modify_time 更新时间, purpose 实验目的,
principle 实验原理, equipment 实验材料, step 实验步骤, result 结果, discussion 讨论,
table_path 表格路径json, chart_path 图片路径json. 
'''
sql_create_table = '''create table if not exists record
                        (ID integer primary key autoincrement,
                        enable boolean default 1,
                        subject text not null,
                        object text not null,
                        method text not null,
                        researcher text not null,
                        create_time TimeStamp default (datetime('now','localtime')),
                        modify_time TimeStamp default (datetime('now','localtime')),
                        purpose text,
                        principle text,
                        equipment text,
                        step text,
                        result text,
                        discussion text,
                        table_path text,
                        chart_path text)'''

sql_insert_example = '''insert into record(subject, object, method, researcher, purpose) values
                          ('生长曲线实验示例', 'E.coli', '比浊法', '来自豆丁网示例', '1.练习无菌操作技术，学习液体培养基配制和接种方法；\n
                          2.掌握利用细菌悬液浑浊度间接测定细菌生长的方法；\n3.了解细菌生长曲线特征，测定细菌繁殖代时；') '''

sql_select_example = '''select * from record where ID = 1'''

sql_select_records = '''select ID, subject, object, method, researcher, create_time from record where enable = 1'''

sql_disable_arecord = '''update record set enable = 0 where ID = ?'''

sql_insert_arecord = '''insert into record(subject, object, method, researcher) values (?, ?, ?, ?)'''

sql_update_arecord = '''update record set modify_time = (datetime('now','localtime')), purpose = ?, principle = ?, 
                          equipment = ?, step = ?, result = ?, discussion = ? where ID = ?'''
