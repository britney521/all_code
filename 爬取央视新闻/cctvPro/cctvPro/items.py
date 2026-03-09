# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CctvproItem(scrapy.Item):
    title = scrapy.Field()
    # 正文
    content = scrapy.Field()
    # 文章发布时间
    publish_time = scrapy.Field()
    # 爬取时间
    spider_time = scrapy.Field()
    # 编辑
    author = scrapy.Field()
    # 来源
    articleSource = scrapy.Field()
    # 链接
    article_url = scrapy.Field()

class  CctvjunshiproItem(scrapy.Item):
    title = scrapy.Field()
    # 正文
    content = scrapy.Field()
    # 文章发布时间
    publish_time = scrapy.Field()
    # 爬取时间
    spider_time = scrapy.Field()
    # 编辑
    author = scrapy.Field()
    # 来源
    articleSource = scrapy.Field()
    # 链接
    article_url = scrapy.Field()
class  CctvrenwuproItem(scrapy.Item):
    title = scrapy.Field()
    # 正文
    content = scrapy.Field()
    # 文章发布时间
    publish_time = scrapy.Field()
    # 爬取时间
    spider_time = scrapy.Field()
    # 编辑
    author = scrapy.Field()
    # 来源
    articleSource = scrapy.Field()
    # 链接
    article_url = scrapy.Field()