# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json
main_link = 'https://api.github.com'
name_user=input('Введите имя пользователя github')
url='/users/'+name_user+'/repos'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
response=requests.get(main_link+url,headers=header)
if response.ok:
    list_repos=json.loads(response.text)
    n = 1
    for i in list_repos:
        print(str(n)+ ' '+ i['name'])
        n+=1
    with open(name_user + '.json', "w", encoding="utf-8") as f:
        f.write(response.text)



