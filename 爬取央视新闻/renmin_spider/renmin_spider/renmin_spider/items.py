# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#与数据库完全一致
class RenminSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    #标题
    title = scrapy.Field()
    #正文
    content = scrapy.Field()
    #文章发布时间
    publish_time = scrapy.Field()
    #爬取时间
    spider_time = scrapy.Field()
    #作者
    author =scrapy.Field()
    #来源
    articleSource =scrapy.Field() 
    #链接
    article_url =scrapy.Field()

