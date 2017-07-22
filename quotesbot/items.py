# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ParkItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()

    history = scrapy.Field()

    # basicinfo
    hours = scrapy.Field()
    fees = scrapy.Field()
    goodsandservices = scrapy.Field()

    # things2do
    # need to be more detailed
    things2do = scrapy.Field()

    # news
    news = scrapy.Field()
    nature = scrapy.Field()

    weather = scrapy.Field()

