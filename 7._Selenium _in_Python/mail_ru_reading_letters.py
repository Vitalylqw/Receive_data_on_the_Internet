# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NewPassword172
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

login = 'study.ai_172@mail.ru'
password = 'NextPassword172'


def get_date(text):
    if 'Вчера' in text:
        return pendulum.yesterday('Europe/Moscow').format('DD.MM.YYYY')
    if 'Сегодня' in text:
        return pendulum.today('Europe/Moscow').format('DD.MM.YYYY')
    date_split= text.split(',')[0].split()
    if date_split[1]=='января':
        month='01'
    elif date_split[1]=='февраля':
        month='02'
    elif date_split[1] == 'марта':
        month = '03'
    elif date_split[1]=='апреля':
        month='04'
    elif date_split[1]=='мая':
        month='05'
    elif date_split[1]=='июня':
        month='06'
    elif date_split[1] == 'июля':
        month = '07'
    elif date_split[1]=='августа':
        month='08'
    elif date_split[1]=='сентября':
        month='09'
    elif date_split[1]=='октября':
        month=10
    elif date_split[1]=='ноября':
        month=11
    elif date_split[1]=='декбря':
        month=12
    if len(date_split)==2:
        return f'{date_split[0]}.{month}.{pendulum.now().year}'
    if len(date_split)==3:
        return f'{date_split[0]}.{month}.{date_split[2]}'

def get_data_from_letter(driver):
    data_leter = {}
    data_leter['data'] = get_date(WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, 'letter__date'))).text)
        # data_leter['data']=get_date(driver.find_element_by_class_name('letter__date').text)
    data_leter['from'] = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))).get_attribute('title')
        # driver.find_element_by_class_name('letter-contact').get_attribute('title')
    data_leter['subject'] = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, 'h2'))).text
        # driver.find_element_by_tag_name('h2').text
    data_leter['leter'] = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, 'letter-body'))).text
        # driver.find_element_by_tag_name('letter-body').text
    return data_leter


list_leters=[]
driver=webdriver.Chrome()
driver.get('https://mail.ru')
time.sleep(2)
elem = driver.find_element_by_id('mailbox:login')
time.sleep(2)
elem.send_keys(login)
elem.send_keys(Keys.RETURN)
time.sleep(2)
elem = driver.find_element_by_id('mailbox:password')
elem.send_keys(password)
elem.send_keys(Keys.RETURN)
# time.sleep(5)
leter = WebDriverWait(driver,20).until(ec.presence_of_element_located((By.CLASS_NAME,'js-tooltip-direction_letter-bottom')))
# leter=driver.find_element_by_class_name("js-tooltip-direction_letter-bottom")+

try:
    driver.get(leter.get_attribute('href'))
    list_leters.append(get_data_from_letter(driver))
    elem = WebDriverWait(driver,20).until(ec.presence_of_element_located((By.CLASS_NAME,'portal-menu-element_next')))
except  Exception as e:
    print('Писем нет',e ,sep="\n")

while True:
    try:
        elem.click()
        time.sleep(5)
        list_leters.append(get_data_from_letter(driver))
        elem =  WebDriverWait(driver,20).until(ec.presence_of_element_located((By.CLASS_NAME,'portal-menu-element_next')))
        # driver.find_element_by_class_name('portal-menu-element_next')
    except Exception as e:
        print('Письма кончились',e ,sep="\n")
        break
pprint(list_leters)

client = MongoClient('localhost:27017')
db = client.mail
collection = db.mailru
try:
    collection.drop()
    collection.insert_many(list_leters)
except Exception as e:
    print(e)




