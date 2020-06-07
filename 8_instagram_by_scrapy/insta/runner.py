# 1)Написать приложение, которое будет проходиться по указанному списку пользователей и собирать данные о его подписчиках и подписках.
# 2) По каждому пользователю, который является подписчиком или на которого подписан исследуемый объект нужно извлечь имя,
# id и фото (остальные данные по желанию). Фото можно дополнительно скачать.
# 3) Собранные данные необходимо сложить в базу данных.
# 4) Написать запрос к базе, который вернет список подписчиков указанного пользователя
# 5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from insta.spiders.insta_one import InstaOneSpider
from insta import settings

if __name__ == '__main__':
    list_usrs=['miapassi','totoshka_doroshka']
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaOneSpider,list_usrs)
    process.start()


# username: ivanovsergei9696
# enc_password: #PWD_INSTAGRAM_BROWSER:10:1591549038:AZRQAB8Rak7Iu6YpSJEaDTp4aey2r589fKI5sTq8oeX5sdUZ7aqv0p+FkpJe03NdMsW89AeEuF5t0dI4CU6WZCh4O880rWQt4254WiPbHrtTFONScxZEyty1djea1hNF36pERBPY75CD93bB
# queryParams: {"oneTapUsers":"[\"37228182439\"]"}
# optIntoOneTap: false