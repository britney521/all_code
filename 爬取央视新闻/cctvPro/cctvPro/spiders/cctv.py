import scrapy

import re
import datetime
import time
import json
from cctvPro.items import CctvproItem


class CctvSpider(scrapy.Spider):
    name = 'cctv'
    # allowed_domains = ['news.cctv.com']

    start_urls = [
        "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_{0}.jsonp?",     #国际
                  "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_{0}.jsonp?",  #国内
                  "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/news_{0}.jsonp?",#新闻
                  "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/society_{0}.jsonp?"#社会
                  "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/law_{0}.jsonp?",#法制
                  "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/ent_{0}.jsonp?",#文娱
               " https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/tech_{0}.jsonp?",#科技
            "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/life_{0}.jsonp?",#生活

    ]
    headers = {
        'Host': 'news.cctv.com',
        'Origin': 'https://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            for i in range(1,10):
                yield scrapy.Request(url.format(i), self.parse, dont_filter=True)

    def parse(self, response):
        url = response.url

        data_list = response.json()["data"]["list"]
        # print(response.xpath("//body").extract())
        for item in data_list:
            tmpurl = item.get("url", "")
            title = item.get("title", "")
            publish_time = item.get("focus_date","")

            print(tmpurl)
            # tmpurl = tools.getpath(tmpurl, response.url)
            yield scrapy.Request(url=tmpurl, callback=self.parse_detal,meta={"tmpurl": tmpurl,"title":title,"publish_time":publish_time} ,dont_filter=True)
        # for i in range(1,7):
        #     yield scrapy.Request(url.format(i), self.parse, dont_filter=True)
    def parse_detal(self, response):
        item = CctvproItem()
        # print(response.text)
        item["title"] = response.meta.get("title","")
        content = response.css('#content_area p::text').extract()
        item["content"] = "".join(content).strip("\n\u3000\u3000")
        # item["content"] = re.sub(r"<[^<>]+?>", "", content)
        publish = response.css('.title_area div.info::text').extract_first().strip()
        match_obj = re.match("来源：(.*?)  |  (.*?)",publish)
        if match_obj:
            item["articleSource"] = match_obj.group(1)
        else:
            item["articleSource"] ="界面新闻"
        publish_time = response.meta.get("publish_time","")
        # item["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(publish_time))
        item["publish_time"] = time.strftime(

            "%Y/%m/%d %H:%M:%S", time.strptime(publish_time, "%Y-%m-%d %H:%M:%S"))

        item['spider_time'] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        author = response.css(
            'div.zebian span#zb::text').extract_first()

        item['author'] = author.replace("责任编辑：", "")

        # item['articleSource'] = response.xpath(
        #     '//meta[@property="article:author"]/@content').extract_first()

        item['article_url'] = response.meta.get("tmpurl","")


        return item
