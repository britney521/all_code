
import scrapy
import re
import datetime
import time
from renmin_spider.items import RenminSpiderItem


class sina(scrapy.Spider):
    name = 'sina'
    def start_requests(self):
        base = ["http://news.sina.com.cn"]
        start_urls = ["https://news.cctv.com/world/?","https://news.cctv.com/china/?"]

        for url in start_urls:
            yield scrapy.Request(url,self.parse_dictionary, dont_filter=True)

    def parse_dictionary(self, response):
        data_list = response.json()["data"]["list"]
        #print(response.xpath("//body").extract())
        for item in data_list:
            tmpurl = item.get("url","")
            print(tmpurl)
            # tmpurl = tools.getpath(tmpurl, response.url)
            yield scrapy.Request(tmpurl,self.parse_article,dont_filter=True)


        



    def parse_article(self, response):
        item = RenminSpiderItem()
        item["title"] = response.xpath('//*[@id="title_area"]/h1').extract_first()
        content = response.xpath('//div[@class="article"]').extract_first()
        item["content"] = re.sub(r"<[^<>]+?>", "", content)
        publish_time = response.xpath('//span[@class="date"]/text()').extract_first()
        # item["publish_time"] = time.strftime(publish_time, '%Y年%b月%d日 %H:%M')

        item["publish_time"] = time.strftime(
            
            "%Y/%m/%d %H:%M:%S", time.strptime(publish_time, "%Y年%m月%d日 %H:%M"))

        item['spider_time'] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        author = response.xpath(
            '//p[@class="show_author"]/text()').extract_first()

        item['author'] = author.replace("责任编辑：","")

        item['articleSource'] = response.xpath(
            '//meta[@property="article:author"]/@content').extract_first()

        item['article_url'] = response.xpath(
            '//meta[@property="og:url"]/@content').extract_first()

        return item