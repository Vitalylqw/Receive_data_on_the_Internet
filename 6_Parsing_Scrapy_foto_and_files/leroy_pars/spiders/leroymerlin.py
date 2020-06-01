# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroy_pars.items import LeroyParsItem

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    characteristics = {}

    def __init__(self,text):
        self.start_urls = [f'https://spb.leroymerlin.ru/search/?q={text}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        item_pages = response.xpath('//a[@class="link-wrapper"]/@href').extract()
        for link in item_pages:
            yield response.follow(link,callback=self.item_pars)
        yield response.follow(next_page,callback=self.parse)

    def item_pars(self,response:HtmlResponse):
        loader=ItemLoader(item=LeroyParsItem(), response=response)
        loader.add_xpath('name','//h1/text()')
        loader.add_xpath('artikul', '//span[@itemprop="sku"]/@content')
        loader.add_xpath('photos','//uc-pdp-media-carousel/picture/source[1]/@data-origin')
        loader.add_xpath('price','//span[@slot="price"]/text()')
        loader.add_value('characteristics', response.xpath('//div[@class="def-list__group"]'))
        loader.add_value('link', response.url)
        yield loader.load_item()




