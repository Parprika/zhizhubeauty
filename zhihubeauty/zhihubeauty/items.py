# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BeautyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'beauty'
    url_token = Field()
    name = Field()
    gender = Field()
    avatar_url = Field()
    headline = Field()
    followers = Field()


class RelationItem(Item):
    collection = 'beauty'
    url_token = Field()
    followers = Field()
