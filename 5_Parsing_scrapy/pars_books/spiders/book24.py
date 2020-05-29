# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from pars_books.items import ParsBooksItem

class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']

    def __init__(self,tema):
        self.start_urls = [f'https://book24.ru/search/?q={tema}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="catalog-pagination__item _text js-pagination-catalog-item"]/@href').extract_first()
        books_links = response.xpath('//a[@class="book__image-link js-item-element ddl_product_link"]/@href').extract()
        for link in books_links:
            yield  response.follow(link,callback=self.item_pars)
        yield response.follow(next_page, callback=self.parse)

    def item_pars(self,response:HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//div[@class="item-actions__price"]/b/text()').extract_first()
        discount_price =response.xpath('//div[@class="item-actions__price"]/b/text()').extract_first()
        rating =response.xpath('//div[@class="live-lib__rate-value"]/text()').extract_first()
        link = response.url
        autor = response.xpath('//a[@class="item-tab__chars-link js-data-link"]/text()').extract()
        source = self.allowed_domains[0]
        yield ParsBooksItem(name=name, price=price, discount_price=discount_price, rating=rating,  link=link,source=source,autor=autor)