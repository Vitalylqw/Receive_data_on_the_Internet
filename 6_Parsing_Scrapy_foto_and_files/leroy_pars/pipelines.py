# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class LeroyParsPipeline:
    client = MongoClient('localhost:27017')
    mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        my_data = item._values
        collection_mongo = self.mongo_base[spider.name]
        collection_mongo.update_one({'artikul': my_data['artikul']}, {'$set': my_data}, upsert=True)
        return item


class get_characteristics:
    def process_item(self, item, spider):
        data={}
        for tag in item['characteristics']:
            data[tag.xpath('./dt/text()').extract_first()]=tag.xpath('./dd/text()').extract_first().strip()
        item['characteristics'] =data
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            n=1
            for img in item['photos']:
                try:
                    yield scrapy.Request(img,meta={'art':item["artikul"],'numer':str(n)})
                    n+=1
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        return f"{request.meta['art']}/{request.meta['numer']}.jpg"


    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item