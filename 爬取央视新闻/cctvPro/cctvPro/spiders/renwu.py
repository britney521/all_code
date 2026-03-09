# -*- coding: UTF-8 -*- #
"""
@author:britlee
@file:renwu.py
@time:2022/07/10
"""

import scrapy

import re
import datetime
import time
import json
from cctvPro.items import CctvrenwuproItem


class CctvrenwuSpider(scrapy.Spider):
    name = 'renwu'
    url = "https://api.cntv.cn/NewArticle/getArticleListByPageId?serviceId=pcnews&id=PAGEEbwoCRG76wMgJefnNvVh170118&p={0}&n=100"
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    def start_requests(self):

        for i in range(1,10):

            yield scrapy.Request(self.url.format(i), self.parse,headers=self.headers,dont_filter=True)

    def parse(self, response):
        data_list = response.json()["data"]["list"]
        for item in data_list:
            tmpurl = item.get("url", "")
            title = item.get("title", "")
            publish_time = item.get("focus_date", "")

            print(tmpurl)
            yield scrapy.Request(url=tmpurl, callback=self.parse_detal,meta={"tmpurl": tmpurl,"title":title,"publish_time":publish_time} ,dont_filter=True)

    def parse_detal(self, response):
        item = CctvrenwuproItem()
        # print(response.text)
        item["title"] = response.meta.get("title","")
        content = response.css('#content_area p::text').extract()
        item["content"] = "".join(content).strip("\u3000\u3000")
        # item["content"] = re.sub(r"<[^<>]+?>", "", content)
        publish = response.css('.title_area div.info::text').extract_first().strip()
        match_obj = re.match("来源：(.*?)  |  (.*?)",publish)
        if match_obj:
            item["articleSource"] = match_obj.group(1)
        publish_time = int(response.meta.get("publish_time",""))/1000
        # item["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(publish_time))
        item["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(publish_time))

        item['spider_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        author = response.css(
            'div.zebian span#zb::text').extract_first()

        item['author'] = author.replace("责任编辑：", "")

            # item['articleSource'] = response.xpath(
            #     '//meta[@property="article:author"]/@content').extract_first()

        item['article_url'] = response.meta.get("tmpurl","")


        return item
