from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroy_pars import settings
from leroy_pars.spiders.leroymerlin import LeroymerlinSpider

if __name__ == '__main__':
    text='перфоратор'
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, text=text)
    process.start()