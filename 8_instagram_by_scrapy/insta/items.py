# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Owner_id = scrapy.Field()
    type = scrapy.Field()
    subscriber_id = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    photo = scrapy.Field()
    post_data = scrapy.Field()
    parser_user_name=scrapy.Field()

