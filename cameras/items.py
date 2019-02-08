# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CamerasItem(scrapy.Item):
    T = scrapy.Field()
    uid = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    spider = scrapy.Field()
