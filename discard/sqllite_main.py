# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : sqllite_main.py
# Time       ：2022/4/5 13:33
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：
"""
import sqlite3
db_filepath = 'records.db'

# conn = sqlite3.connect('test.db')
# curs = conn.cursor()
# curs.execute('''CREATE TABLE COMPANY
#        (ID INT PRIMARY KEY     NOT NULL,
#         NAME           TEXT    NOT NULL,
#         AGE            INT     NOT NULL,
#         ADDRESS        CHAR(50),
#         SALARY         REAL);''')
# print("数据表创建成功")
# conn.commit()
# conn.close()

# conn = sqlite3.connect('test.db')
# c = conn.cursor()
# print ("数据库打开成功")
#
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (1, 'Paul', 32, 'California', 20000.00 )")
#
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
#
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
#
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
#
# conn.commit()
# print ("数据插入成功")
# conn.close()

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
sql_insert_record = '''insert into record
                        (enable, subject, bacteria, method) values
                        (1, '生长曲线实验示例', 'E.coli', '比浊法') '''
conn.execute(sql_insert_record)
sql_select_records = '''select ID, subject, bacteria, method, create_time
                        from record where enable = 1'''
rows = conn.execute(sql_select_records)

conn.commit()
conn.close()