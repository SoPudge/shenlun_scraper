# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ShenlunScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    pub_date = scrapy.Field()
    spider_name = scrapy.Field()
