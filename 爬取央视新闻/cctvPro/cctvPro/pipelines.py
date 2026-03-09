# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class CctvproPipeline:
    def __init__(self):
        self.f = open('cctv.csv', 'a', encoding='utf-8', newline='')
        self.file_name = ['', 'content', 'publish_time', 'spider_time', 'author', 'articleSource', 'article_url']
        self.writer = csv.DictWriter(self.f, fieldnames=self.file_name)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(dict(item))

        print(item)

        # def process_item(self, item, spider):
        #     appbk_sql.insert_data(item, "news_info")
        #     return item

    def close_spider(self, spider):
        self.f.close()
