# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose

def get_price(value:list):
    try:
        value = int(value[0].replace(' ',''))
    except Exception as e:
        print(e, "Невозвожно преобразовать цену", sep='\n')
    return  value

def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    return value


class LeroyParsItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    artikul = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(get_price))
    # price = scrapy.Field(output_processor=TakeFirst())
    link= scrapy.Field(output_processor=TakeFirst())
    characteristics = scrapy.Field()

