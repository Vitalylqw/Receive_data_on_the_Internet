# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
#     Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.chrome.options import Options
import time
import pendulum
from pprint import pprint
import json;

list_leters=[]
driver=webdriver.Chrome()
driver.get('https://www.mvideo.ru/')
time.sleep(10)
pages=1
while True:
    try:
        time.sleep(5)
        # button = driver.find_elements_by_xpath("//a[@class='next-btn sel-hits-button-next']")
        button = WebDriverWait(driver,10).until(ec.presence_of_element_located((By.XPATH,'//div[@data-init="ajax-category-carousel"][2]//a[@class="next-btn sel-hits-button-next"]')))
        # button = driver.find_element_by_class_name('special-offers__more-btn')
        button.click()
        pages+=1
    except Exception as e:
        print(e,f'всего страниц {pages}')
        break

bloks= driver.find_elements_by_xpath("//div[@data-sel='new_cart-carousel-gallery_accessories']")
goods=bloks[1].find_elements_by_xpath(".//li[@class='gallery-list-item height-ready']//a[@data-product-info]")


client = MongoClient('localhost:27017')
db = client.goods
collection = db.mvideo
collection.drop()
for i in goods:
    collection.insert_one(json.loads(i.get_attribute('data-product-info')))


