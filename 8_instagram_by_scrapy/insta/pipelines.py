# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class InstaPipeline:
    client = MongoClient('localhost:27017')
    mongo_base = client.insta
    def process_item(self, item, spider):
        my_data = item._values
        collection_mongo = self.mongo_base['communication']
        collection_mongo.update_one({'$and' :[{'Owner_id': my_data['Owner_id']},{'subscriber_id':my_data['subscriber_id']},{'type':my_data['type']}]}, {'$set': my_data}, upsert=True)
        return item  # -*- coding: utf-8 -*-


class InstPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['photo'],meta={'name':item["full_name"]})
        return item
    def file_path(self, request, response=None, info=None):
        return f"{request.meta['name']}/foto.jpg"