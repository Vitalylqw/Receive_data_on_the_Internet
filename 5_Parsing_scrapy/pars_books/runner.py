from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from pars_books import settings
from pars_books.spiders.labirint import LabirintSpider
from pars_books.spiders.book24 import Book24Spider

if __name__ == '__main__':
    tema = 'Программист'
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(LabirintSpider,tema=tema)
    process.crawl(Book24Spider, tema=tema)
    process.start()