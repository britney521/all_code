# -*- coding: UTF-8 -*- #
"""
@author:britlee
@file:main.py
@time:2022/07/10
"""

from scrapy.cmdline import execute
import sys,os
#添加系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','cctv'])   #’--nolog‘  无日志  '-o','./article.csv'
#执行命令行
# execute(['scrapy','crawl','junshi'])   #’--nolog‘  无日志  '-o','./article.csv'
# execute(['scrapy','crawl','renwu'])   #’--nolog‘  无日志  '-o','./article.csv'
print(os.path.abspath(__file__))
