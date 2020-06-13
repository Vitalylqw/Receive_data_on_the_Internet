# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from insta.items import InstaItem

class InstaOneSpider(scrapy.Spider):
    name = 'insta_one'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = 'ivanovsergei9696'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1591549038:'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    hash_subscribers = 'c76146de99bb02f6415203be841dd25a'
    hash_ssubscriptions= 'd04b0a864b4b54837c0d870b0e77e076'

    def __init__(self,parser_users):
        self.parser_users=parser_users

    def parse(self, response):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.parse_user,
            formdata={'username': self.insta_login,
                      'enc_password': self.insta_pass},
            headers={'X-CSRFToken': csrf_token}
        )

    def parse_user(self, response):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for parser_user in self.parser_users:
                yield response.follow(
                    f'/{parser_user}',
                    callback = self.user_data_parse,
                    cb_kwargs={'parser_user': parser_user,
                               'parser_user_name':parser_user}
                )
        else:
            print('авторизация не прошла')
            return


    def user_data_parse(self, response,parser_user,parser_user_name):
        user_id = self.fetch_user_id(response.text, parser_user)
        variables = {"id": user_id,
                     "include_reel": True,
                     "fetch_mutual": False,
                     "first": 50}
        url_subscribers = f'{self.graphql_url}query_hash={self.hash_subscribers}&{urlencode(variables)}'
        url_subscriptions = f'{self.graphql_url}query_hash={self.hash_ssubscriptions}&{urlencode(variables)}'
        yield response.follow(
            url_subscribers,
            callback = self.subscribers_parse,
            cb_kwargs= {'user_id':user_id,
                        'variables': deepcopy(variables),
                        'parser_user_name':parser_user_name})
        yield response.follow(
            url_subscriptions,
            callback=self.subscriptions_parse,
            cb_kwargs={'user_id': user_id,
                       'variables': deepcopy(variables),
                       'parser_user_name': parser_user_name})

    def subscribers_parse(self, response, user_id, variables,parser_user_name):
        j_body = json.loads(response.text)
        subscribers = j_body.get('data').get('user').get('edge_followed_by').get('edges')
        for subscriber in subscribers:
            item = InstaItem(
                parser_user_name = parser_user_name,
                Owner_id=user_id,
                type = "subscriber",
                subscriber_id = subscriber['node']['id'],
                username=subscriber['node']['username'],
                full_name = subscriber['node']['full_name'],
                photo=subscriber['node']['profile_pic_url'],
                post_data=subscriber['node'])
            yield item
        page_info = j_body.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url_subscribers = f'{self.graphql_url}query_hash={self.hash_subscribers}&{urlencode(variables)}'
            yield response.follow(
                url_subscribers,
                callback=self.subscribers_parse,
                cb_kwargs={'user_id': user_id,
                           'variables': deepcopy(variables),
                           'parser_user_name' : parser_user_name})

    def subscriptions_parse(self, response, user_id, variables,parser_user_name):
        j_body = json.loads(response.text)
        subscriptions = j_body.get('data').get('user').get('edge_follow').get('edges')
        for subscription in subscriptions:
            item = InstaItem(
                parser_user_name = parser_user_name,
                Owner_id=user_id,
                type = "subscription",
                subscriber_id = subscription['node']['id'],
                username=subscription['node']['username'],
                full_name = subscription['node']['full_name'],
                photo=subscription['node']['profile_pic_url'],
                post_data=subscription['node'])
            yield item
        page_info = j_body.get('data').get('user').get('edge_follow').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url_subscriptions = f'{self.graphql_url}query_hash={self.hash_ssubscriptions}&{urlencode(variables)}'
            yield response.follow(
                url_subscriptions,
                callback=self.subscriptions_parse,
                cb_kwargs={'user_id': user_id,
                           'variables': deepcopy(variables),
                           'parser_user_name' : parser_user_name})


    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
