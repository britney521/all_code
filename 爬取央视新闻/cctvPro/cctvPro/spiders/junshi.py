# -*- coding: UTF-8 -*- #
"""
@author:britlee
@file:junshi.py
@time:2022/07/10
"""
import scrapy

import re
import datetime
import time
import json
from cctvPro.items import CctvjunshiproItem


class CctvSpider(scrapy.Spider):
    name = 'junshi'
    url = "https://military.cctv.com/data/index.json"
    headers = {
        'Host': 'news.cctv.com',
        'Origin': 'https://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    def start_requests(self):

        yield scrapy.Request(self.url, self.parse, dont_filter=True)

    def parse(self, response):
        data_list = response.json()["rollData"]
        for item in data_list:
            tmpurl = item.get("url", "")
            title = item.get("title", "")
            publish_time = item.get("dateTime", "")

            print(tmpurl)
            yield scrapy.Request(url=tmpurl, callback=self.parse_detal,meta={"tmpurl": tmpurl,"title":title,"publish_time":publish_time} ,dont_filter=True)

    def parse_detal(self, response):
        item = CctvjunshiproItem()
        # print(response.text)
        item["title"] = response.meta.get("title","")
        content = response.css('#content_area p::text').extract()
        item["content"] = "".join(content).strip("\u3000\u3000")
        # item["content"] = re.sub(r"<[^<>]+?>", "", content)
        publish = response.css('.title_area div.info::text').extract_first()
        match_obj = re.match("来源：(.*?)  |  (.*?)",publish)
        if match_obj:
            item["articleSource"] = match_obj.group(1)
        else:
            item["articleSource"] ="界面新闻"
        publish_time = response.meta.get("publish_time","")
        # item["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(publish_time))
        item["publish_time"] = time.strftime(

            "%Y/%m/%d %H:%M:%S", time.strptime(publish_time, "%Y-%m-%d %H:%M"))

        item['spider_time'] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        author = response.css(
            'div.zebian span#zb::text').extract_first()

        item['author'] = author.replace("责任编辑：", "")

            # item['articleSource'] = response.xpath(
            #     '//meta[@property="article:author"]/@content').extract_first()

        item['article_url'] = response.meta.get("tmpurl","")


        return item