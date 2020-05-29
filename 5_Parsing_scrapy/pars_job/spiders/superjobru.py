# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from pars_job.items import ParsJobItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']

    def __init__(self,vacansy):
        self.start_urls = [f'https://spb.superjob.ru/vacancy/search/?keywords={vacansy}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        job_links = response.xpath("//a[contains(@class,'_6AfZ9')]/@href").extract()
        for link in job_links:
            yield response.follow(link, callback=self.vacansy_pars)
        yield response.follow(next_page, callback=self.parse)
    def vacansy_pars(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath('//div[@class="_3MVeX"]/span/text()').extract()
        link = response.url
        employer = response.xpath("//a/h2/text()").extract()
        source = self.allowed_domains[0]
        yield ParsJobItem(name=name, salary=salary, link=link, employer=employer, source=source)