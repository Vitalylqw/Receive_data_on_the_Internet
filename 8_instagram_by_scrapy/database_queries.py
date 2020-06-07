# 4) Написать запрос к базе, который вернет список подписчиков указанного пользователя
# 5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

from pymongo import MongoClient


client = MongoClient('localhost:27017')
db = client.insta.communication

def subscribers(user):
    my_list= db.find({'parser_user_name':user,'type':'subscriber'})
    for i in my_list:
        print(i['full_name'])

def subscriptions(user):
    my_list= db.find({'parser_user_name':user,'type':'subscription'})
    for i in my_list:
        print(i['full_name'])


# subscribers('miapassi')
subscriptions('miapassi')


