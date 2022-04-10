# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : findstr.py
# Time       ：2022/4/10 20:46
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：
"""
str = "this is really a string example....wow!!!"
substr = "is"

print (str.rfind(substr))
print (str.rfind(substr, 0, 10))
print (str.rfind(substr, 10, 0))

print (str.find(substr))
print (str.find(substr, 0, 10))
print (str.find(substr, 10, 0))