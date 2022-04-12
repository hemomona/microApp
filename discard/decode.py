# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : decode.py
# Time       ：2022/4/12 17:32
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：
"""
s= '1_%u56FE9.%u8F6C%u901F%u5BF9%u751F%u957F%u66F2%u7EBF%u5F71%u54CD.png'
print(s.replace('%', '\\').lower())