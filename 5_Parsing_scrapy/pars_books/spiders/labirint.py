# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from pars_books.items import ParsBooksItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']

    def __init__(self,tema):
        self.start_urls = [f'https://www.labirint.ru/search/{tema}/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.pagination-next__text::attr(href)').extract_first()
        books_links = response.xpath('//a[@class="cover"]/@href').extract()
        for link in books_links:
            yield  response.follow(link,callback=self.item_pars)
        yield response.follow(next_page, callback=self.parse)

    def item_pars(self,response:HtmlResponse):
        name = response.xpath('//span[@class="only_desc"]/text()').extract_first()
        price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').extract_first()
        discount_price =response.xpath('//span[@class="buying-priceold-val-number"]/text()').extract_first()
        rating =response.xpath("//div[@id='rate']/text()").extract_first()
        link = response.url
        autor = response.xpath('//div[@class="authors"]/a/text()').extract()
        source = self.allowed_domains[0]
        yield ParsBooksItem(name=name, price=price, discount_price=discount_price, rating=rating,  link=link,source=source,autor=autor)