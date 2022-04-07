# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : log.py
# Time       ：2022/4/7 10:04
# Author     ：Jago
# Email      ：18146856052@163.com
# version    ：python 3.7
# Description：
"""
import logging.config

# logging.debug("This is a debug log.")
# logging.info("This is a info log.")
# logging.warning("This is a warning log.")
# logging.error("This is a error log.")
# logging.critical("This is a critical log.")

# logging.basicConfig(level=logging.DEBUG #设置日志输出格式
#                     ,filename="demo.log" #log日志输出的文件位置和文件名
#                     ,filemode="a" #文件的写入格式，w为重新写入文件，默认是追加
#                     ,format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s" #日志输出的格式
#                     # -8表示占位符，让输出左对齐，输出长度都为8位
#                     ,datefmt="%Y-%m-%d %H:%M:%S") #时间输出的格式
#
# logging.debug("This is  DEBUG !!")
# logging.info("This is  INFO !!")
# logging.warning("This is  WARNING !!")
# logging.error("This is  ERROR !!")
# logging.critical("This is  CRITICAL !!")
#
# #在实际项目中，捕获异常的时候，如果使用logging.error(e)，只提示指定的logging信息，不会出现
# #为什么会错的信息，所以要使用logging.exception(e)去记录。
#
# try:
#     3/0
# except Exception as e:
#     # logging.error(e)
#     logging.exception(e)
# 读取日志配置文件内容
logging.config.fileConfig('logging.conf')

# 创建一个日志器logger
logger = logging.getLogger('simpleExample')

# 日志输出
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
