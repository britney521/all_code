# -*- coding: UTF-8 -*- #
"""
@author:britlee
@file:main.py
@time:2022/07/10
"""

from scrapy.cmdline import execute
import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','sina'])   #’--nolog‘  无日志  '-o','./article.csv'
print(os.path.abspath(__file__))
