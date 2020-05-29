# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParsBooksItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    employer= scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    salary = scrapy.Field()
    source= scrapy.Field()
    pass
