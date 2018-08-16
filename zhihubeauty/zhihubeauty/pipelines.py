# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from zhihubeauty.items import BeautyItem, RelationItem


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[BeautyItem.collection].create_index([('url_token',
                                                      pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, BeautyItem):
            self.db[item.collection].update({
                'url_token': item.get('url_token')
            }, {'$set': item}, True)
        if isinstance(item, RelationItem):
            self.db[item.collection].update({
                'url_token': item.get('url_token')
            }, {'$addToSet': {
                'followers': {
                    '$each': item['followers']
                }
            }}, True)
        return item
