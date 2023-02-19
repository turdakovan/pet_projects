import requests
import pandas as pd


url_name = 'https://api.coincap.io/v2/assets'

# получаем данные в виде словаря питона
response_dict_name = requests.get(url_name).json()

# Получаем названия валют: проходимся по списку словарей response_dict_name['data'] и добавляем все i по ключу id
names_assets = []
for i in response_dict_name['data']:
    names_assets.append(i['id'])
    
# основной url
url_first_part = 'https://api.coincap.io/v2/assets/'

result_date_list = []
result_price_list = []
result_name_assets_list = []

# запрос в цикле к api
# подставляем название валюты name в url + интервал в 1 день
# во вложенном цикле парсим список словарей response_dict['data']
# название валюты, дату, price и добавляем в соответствующие списки
for name in names_assets:
    url = url_first_part + name + '/history?interval=d1'
    response_dict = requests.get(url).json()
    for i in range(len(response_dict['data'])):
        result_name_assets_list.append(name)
        result_date_list.append(response_dict['data'][i]['date'])
        result_price_list.append(response_dict['data'][i]['priceUsd'])

        
# формируем словарь для датафрейма на основе списков
result_dict_for_df = {
    'name' : result_name_assets_list,
    'date' : result_date_list,
    'price_usd' : result_price_list
}
# формируем датафрейм
df = pd.DataFrame(result_dict_for_df)

# приводим строку в столбце date к типу datetime
df['date'] = pd.to_datetime(df['date'])

# оставляем в столбце data только дату
df['date'] = df['date'].dt.date

# приводим значения в столбце price_usd к float и округляем
df['price_usd'] = df['price_usd'].astype('float').round(4)

print(df)