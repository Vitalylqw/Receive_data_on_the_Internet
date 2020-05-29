from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from pars_job import settings
from pars_job.spiders.hhru import HhruSpider
from pars_job.spiders.superjobru import SuperjobruSpider

if __name__ == '__main__':
    vacansy = 'Программист'
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider,vacansy=vacansy)
    process.crawl(SuperjobruSpider, vacansy=vacansy)
    process.start()