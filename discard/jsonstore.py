# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : jsonstore.py
# Time       ：2022/4/6 12:39
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：
"""
from kivy.storage.jsonstore import JsonStore

store = JsonStore('hello.json')

# put some values
store.put('tito', name='Mathieu', org='kivy')
store.put('tshirtman', name='Gabriel', age=66)

# using the same index key erases all previously added key-value pairs
store.put('tito', name='Mathieu', age=30)
store.put('tito', age=66)
# get a value using a index key and key
print('tito is', store.get('tito')['age'])
for key, value in store.find(age=66):
    print(key, " ", value)
x = list(x[1] for x in store.find(age=66))
print(x)
print(str(x[0]))


# or guess the key/entry for a part of the key
for item in store.find(name='Gabriel'):
    print('tshirtmans index key is', item[0])
    print('his key value pairs are', str(item[1]))