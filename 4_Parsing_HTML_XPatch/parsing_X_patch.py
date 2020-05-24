# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# * название источника,
# * наименование новости,
# * ссылку на новость,
# * дата публикации
# 2)Сложить все новости в БД

from lxml import html
import pendulum
import requests
from pprint import pprint
from pymongo import MongoClient


class news():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'}

    def get_news_mail(self):
        news=[]
        main_link = 'https://news.mail.ru'
        response = requests.get(main_link, headers = self.header)
        dom = html.fromstring(response.text)
        links=dom.xpath("//div[@class='daynews__item']/a/@href")
        links+=dom.xpath("//a[@class='list__text']/@href")
        for link in links:
            new={}
            new['link']=main_link+link
            if 'http' in link:
                response = requests.get(link, headers=self.header)
            else:
                response = requests.get(main_link+link, headers = self.header)
            dom = html.fromstring(response.text)
            new['source'] =dom.xpath("//span[@class='breadcrumbs__item']//span[@class='link__text']/text()")[0]
            new['name'] =dom.xpath("//h1/text()")[0]
            new['date'] = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0][:10]
            news.append(new)
        return news

    def get_news_yandex(self):
        news = []
        main_link = 'https://yandex.ru'
        response = requests.get(main_link+'/news', headers=self.header)
        dom = html.fromstring(response.text)
        links = dom.xpath("//td[@class='stories-set__item']")
        for link in links:
            new = {}
            new['link'] = main_link + link.xpath(".//h2/a/@href")[0]
            new['name'] = link.xpath(".//h2/a/text()")[0]
            text = link.xpath(".//div[@class='story__date']/text()")[0]
            source = ''
            lst = text.split()
            for i in lst:
                if i == 'вчера' or ':' in i:
                    break
                else:
                    source += i + " "
            source = source.strip()
            new['source'] = source
            if 'вчера' in text:
                new['date'] = pendulum.yesterday('Europe/Moscow').format('DD.MM.YYYY')
            else:
                new['date'] = pendulum.today('Europe/Moscow').format('DD.MM.YYYY')
            news.append(new)
        return news

    def get_news_lenta(self):
        news = []
        main_link = 'https://lenta.ru/'
        response = requests.get(main_link , headers=self.header)
        dom = html.fromstring(response.text)
        links = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']")
        for link in links:
            new = {}
            new['link'] = main_link + link.xpath("./a/@href")[0]
            new['name'] = link.xpath("./a/text()")[0].replace('\xa0',"")
            new['source'] = 'Lenta.ru'
            new['date'] = link.xpath(".//time/@title")[0]
            news.append(new)
        link = dom.xpath("//div[@class='first-item']")[0]
        new = {}
        new['link'] = main_link + link.xpath("./a/@href")[0]
        new['name'] = link.xpath("./h2/a/text()")[0].replace('\xa0'," ")
        new['source'] = 'Lenta.ru'
        new['date'] = link.xpath(".//time/@title")[0]
        news.append(new)
        return news


class insert_to_mongodb():
    def __init__(self, my_db,my_collecton, connect_str='localhost:27017'):
        self.connect_str=connect_str
        self.my_db=my_db
        self.my_collection=my_collecton
    def __connect(self):
        try:
            client = MongoClient(self.connect_str)
            db = client[self.my_db]
            collection = db[self.my_collection]
            return  collection
        except Exception as e:
            print("нет подключения" + str(e))

    def only_insert_all_data(self,my_data):
        cursor=self.__connect()
        cursor.insert_many(my_data)

    def add_new(self,my_data):
        cursor = self.__connect()
        for i in my_data:
            cursor.update_one({'link':i['link']},{'$set':i},upsert=True)



if __name__ == '__main__':
    news=news()
    load=insert_to_mongodb('news','yandex')
    load.add_new(news.get_news_yandex())
    load = insert_to_mongodb('news', 'mail')
    load.add_new(news.get_news_mail())
    load = insert_to_mongodb('news', 'lenta')
    load.add_new(news.get_news_lenta())

