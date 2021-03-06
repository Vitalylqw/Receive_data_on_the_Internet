# -*- coding: utf-8 -*-
from pymongo import MongoClient
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ParsBooksPipeline:
    client = MongoClient('localhost:27017')
    mongo_base = client.books

    def process_item(self, item, spider):
        my_data = item._values
        collection_mongo = self.mongo_base[spider.name]
        collection_mongo.update_one({'link': my_data['link']}, {'$set': my_data}, upsert=True)
        return item  # -*- coding: utf-8 -*-