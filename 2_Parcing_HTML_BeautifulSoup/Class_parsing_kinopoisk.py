from bs4 import BeautifulSoup as bs
import requests
import re


class Parser_kinopoisk():
    def __init__(self):
        self.mian_link = 'https://www.kinopoisk.ru'
    def get_popular_serials(self):
        url = '/popular'
        params = {'quick_filters': 'serials'}
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': '*/*'}
        response = requests.get(self.mian_link + url, headers=header, params=params)
        soup = bs(response.text, 'lxml')
        my_data = soup.find_all('div', {'class': "desktop-rating-selection-film-item"})
        my_list = []
        for link_serial in my_data:
            my_dict = {}
            my_dict['name'] = link_serial.find('p', {'class': 'selection-film-item-meta__name'}).getText()
            my_dict['link'] = self.mian_link + link_serial.find('a', {'class':'selection-film-item-meta__link'})['href']
            my_dict['country'] = link_serial.find('span', {'class':'selection-film-item-meta__meta-additional-item'}).getText()
            my_dict['genre'] = link_serial.find('span', {'class':'selection-film-item-meta__meta-additional-item'}).next_sibling.getText()
            my_dict['yaer'] = re.search(r'\d\d\d\d',link_serial.find('p', {'class': 'selection-film-item-meta__original-name'}).getText())[0]
            my_dict['rating'] = link_serial.find('span', {'class': 'rating__value'}).getText()
            my_list.append(my_dict)
        return my_list

    def get_popular_films(self):
        url = '/popular'
        params = {'quick_filters': 'films'}
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': '*/*'}
        response = requests.get(self.mian_link + url, headers=header, params=params)
        soup = bs(response.text, 'lxml')
        my_data = soup.find_all('div', {'class': "desktop-rating-selection-film-item"})
        my_list = []
        for link_serial in my_data:
            my_dict = {}
            my_dict['name'] = link_serial.find('p', {'class': 'selection-film-item-meta__name'}).getText()
            my_dict['link'] = self.mian_link + link_serial.find('a', {'class':'selection-film-item-meta__link'})['href']
            my_dict['country'] = link_serial.find('span', {'class':'selection-film-item-meta__meta-additional-item'}).getText()
            my_dict['genre'] = link_serial.find('span', {'class':'selection-film-item-meta__meta-additional-item'}).next_sibling.getText()
            my_dict['yaer'] = re.search(r'\d\d\d\d',link_serial.find('p', {'class': 'selection-film-item-meta__original-name'}).getText())[0]
            my_dict['rating'] = link_serial.find('span', {'class': 'rating__value'}).getText()
            my_list.append(my_dict)
        return my_list

my_data =  Parser_kinopoisk()
print(my_data.get_popular_films())
print(my_data.get_popular_serials())





