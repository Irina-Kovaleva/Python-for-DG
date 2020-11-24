#Урок 4

#Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД

import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
main_link = 'https://lenta.ru/'
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)

lenta_news = dom.xpath("//time[@class='g-time']/..")

lenta_news_list = []

for news_item in lenta_news:
    news_item_dict = {}
    source = 'lenta.ru'
    name = news_item.xpath("./time[@class='g-time']/../text()")
    link = news_item.xpath("./time[@class='g-time']/../@href")
    date = news_item.xpath("./time[@class='g-time']/@datetime")

    news_item_dict['source'] = source
    news_item_dict['name'] = name
    news_item_dict['link'] = source + link[0]
    news_item_dict['date'] = date

    lenta_news_list.append(news_item_dict)

pprint(lenta_news_list)

client = MongoClient('127.0.0.1', 27017)
db = client['Lenta.ru_news']
news_db = db.news_db
news_db.insert_many(lenta_news_list)

