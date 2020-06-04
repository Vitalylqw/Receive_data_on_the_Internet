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

list_leters=[]
driver=webdriver.Chrome()
driver.get('https://www.mvideo.ru/')
time.sleep(2)
while True:
    try:
        button = WebDriverWait(driver,10).until(ec.presence_of_element_located((By.CLASS_NAME,'special-offers__more-btn')))
        print(pages)
        # button = driver.find_element_by_class_name('special-offers__more-btn')
        button.click()
        pages+=1
    except:
        print(f'всего страниц {pages}')
        break