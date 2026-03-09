# -*- coding: UTF-8 -*- #
"""
@author:britlee
@file:detail.py
@time:2022/07/10
"""
import requests
import time
import json
url ="https://api.cntv.cn/NewArticle/getArticleListByPageId?serviceId=pcnews&id=PAGEEbwoCRG76wMgJefnNvVh170118&p=6&n=100"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
res = requests.get(url,headers=headers)
res.encoding =res.apparent_encoding
print(res.json())
# # item = time.strftime(time.localtime(1657368561149))
# print(time.localtime(int(1657368561149)/1000))
