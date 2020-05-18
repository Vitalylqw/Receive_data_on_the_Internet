# 1) Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы) с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
#
# *Наименование вакансии
# *Предлагаемую зарплату (отдельно мин. отдельно макс. и отдельно валюту)
# *Ссылку на саму вакансию
# *Сайт откуда собрана вакансия
#
# По своему желанию можно добавить еще работодателя и расположение.
#     Данная структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
import json

class hh():
    def __init__(self,s_key):
        self.mian_link ='https://spb.hh.ru'
        self.s_key=s_key

    def get_vacancies_from_185(self):
        url = '/search/vacancy'
        params = {'area': '2', 'clusters=true': 'true', 'enable_snippets': 'true', 'text': self.s_key,
                  'only_with_salary': 'true', 'salary': '185000', 'from': 'cluster_compensation',
                  'showClusters': 'true'}
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': '*/*'}
        response = requests.get(self.mian_link + url, headers=header, params=params)
        soup = bs(response.text, 'lxml')
        my_data = soup.find_all('div', {'class': "vacancy-serp-item"})
        my_list = []
        self.__get_info_from_page(my_data,my_list)
        page = soup.find('script', {'data-name': 'HH/Pager'})
        num_pages=json.loads(page['data-params'])['pagesCount']
        while num_pages > 1:
            params = {'area': '2', 'clusters=true': 'true', 'enable_snippets': 'true', 'text': self.s_key,
                      'only_with_salary': 'true', 'salary': '185000', 'from': 'cluster_compensation',
                      'showClusters': 'true','page':str((num_pages-1))}
            response = requests.get(self.mian_link + url, headers=header, params=params)
            soup = bs(response.text, 'lxml')
            my_data = soup.find_all('div', {'class': "vacancy-serp-item"})
            self.__get_info_from_page(my_data, my_list)
            num_pages-=1
        return my_list

    def __get_info_from_page(self,my_data,my_list):
        for i in my_data:
            my_dict = {}
            my_dict['name'] = i.find('a', {'class': 'HH-LinkModifier'}).getText()
            my_dict['link'] = i.find('a', {'class': 'HH-LinkModifier'})['href']
            if i.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}):
                my_dict['employer'] = i.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            else:
                my_dict['employer'] = "No Data"
            if i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}):
                salary = self.__get_salary(i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text)
            my_dict['min_salary'] = salary['min']
            my_dict['max_salary'] = salary['max']
            my_dict['currency'] = salary['currency']
            my_dict['source'] = self.mian_link
            my_list.append(my_dict)

    def __get_salary(self,str):
          salary = {}
          if str[:2] == 'от':
              min = re.search(r'[\d\s]+', str)[0]
              min = int(re.sub(r"\s", '', min))
              max = None
          elif str[:2] == 'до':
              max = re.search(r'[\d\s]+', str)[0]
              max = int(re.sub(r"\s", '', max))
              min = None
          else:
              min = re.search(r'[\d\s]+', str)[0]
              min = int(re.sub(r"\s", '', min))
              max = re.search(r'-([\d\s]+)', str)[1]
              max = int(re.sub(r"\s", '', max))
          currency = re.search(r'[A-Zа-я]{3}', str)[0]
          salary['min'] = min
          salary['max'] = max
          salary['currency'] = currency
          return salary




class sj():
    def __init__(self,s_key):
        self.mian_link ='https://spb.superjob.ru'
        self.s_key=s_key

    def get_vacancies_from_with_salary(self):
        url = '/vacancy/search'
        params = { 'keywords': self.s_key, 'payment_defined':'1'}
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': '*/*'}
        response = requests.get(self.mian_link + url, headers=header, params=params)
        soup = bs(response.text, 'lxml')
        my_data = soup.find_all('div', {'class': "iJCa5 f-test-vacancy-item _1fma_ _1JhPh _2gFpt _1znz6 _2nteL"})
        my_list = []
        self.__get_info_from_page(my_data, my_list)
        while soup.find('a', {'rel': 'next'}):
            page=soup.find('a', {'rel': 'next'})['href']
            params = { 'keywords': self.s_key, 'payment_defined':'1'}
            response = requests.get(self.mian_link +page, headers=header, params=params)
            soup = bs(response.text, 'lxml')
            my_data = soup.find_all('div', {'class': "iJCa5 f-test-vacancy-item _1fma_ _1JhPh _2gFpt _1znz6 _2nteL"})
            self.__get_info_from_page(my_data, my_list)
        return my_list

    def __get_info_from_page(self, my_data, my_list):
        for i in my_data:
            my_dict = {}
            my_dict['name'] = i.find('a').getText()
            my_dict['link'] = self.mian_link+i.find('a')['href']
            my_dict['employer'] = i.find('a', {'class':'_25-u7'}).text
            sal=i.find('span', {'class': 'PlM3e'}).text
            salary = self.__get_salary(sal)
            my_dict['min_salary'] = salary['min']
            my_dict['max_salary'] = salary['max']
            my_dict['currency'] = salary['currency']
            my_dict['source'] = self.mian_link
            my_list.append(my_dict)
        # print(my_dict)

    def __get_salary(self, str):
        salary = {}
        if str[:2] == 'от':
            min = re.search(r'[\d\s]+', str)[0]
            min = int(re.sub(r"\s", '', min))
            max = None
            currency = re.search(r'[A-Zа-я]{3}', str)[0]
        elif str[:2] == 'до':
            max = re.search(r'[\d\s]+', str)[0]
            max = int(re.sub(r"\s", '', max))
            min = None
            currency = re.search(r'[A-Zа-я]{3}', str)[0]
        elif '-' in str:
            min = re.search(r'[\d\s]+', str)[0]
            min = int(re.sub(r"\s", '', min))
            max = re.search(r'-([\d\s]+)', str)[1]
            max = int(re.sub(r"\s", '', max))
            currency = re.search(r'[A-Zа-я]{3}', str)[0]
        elif str=="По договорённости":
            min=None
            max=None
            currency = None
        else:
            min = re.search(r'[\d\s]+', str)[0]
            min = int(re.sub(r"\s", '', min))
            max = re.search(r'[\d\s]+', str)[0]
            max = int(re.sub(r"\s", '', max))
            currency = re.search(r'[A-Zа-я]{3}', str)[0]
        salary['min'] = min
        salary['max'] = max
        salary['currency'] = currency
        return salary


vac_hh=hh('Python')
vac_sj = sj('Python')
vacancies = pd.DataFrame(vac_hh.get_vacancies_from_185()+vac_sj.get_vacancies_from_with_salary())
print(vacancies)


