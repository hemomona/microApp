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

conn = sqlite3.connect('test.db')
c = conn.cursor()
print ("数据库打开成功")

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )")

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")

conn.commit()
print ("数据插入成功")
conn.close()