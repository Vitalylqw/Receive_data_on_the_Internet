# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# # Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
from pprint import pprint
import requests
import json
main_link = 'https://api.vk.com/method/'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
url = 'friends.getOnline?v=5.103'
access_token='&access_token=170652d34a81ab45f1b17529397aaf1bc755107270e0a0414d78b5dab58b88af210085dc9d04f10d6b532'
responce = requests.get(main_link+url+access_token, headers=header)
data = json.loads(responce.text)
url='users.get?v=5.103?&user_ids='
for i in data["response"]:
    url+=str(i)+','
responce = requests.get(main_link+url+access_token, headers=header)
with open('frends.json', 'w') as f:
    f.write(responce.text)
pprint(json.loads(responce.text))
