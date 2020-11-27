#Урок 5
#Задание 2
#2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
mvideo = db.mvideo

main_link = 'https://mvideo.ru/'

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get(main_link)

for n in range(3):
    time.sleep(5)
    button = driver.find_element_by_xpath("//a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']")
    button.click()

bestsalers = driver.find_element_by_xpath("//div[text()[contains(.,'Хиты продаж')]]/../../../..")

products = bestsalers.find_elements_by_css_selector('li.gallery-list-item')

list = []

for product in products:
    elem = {}
    data = product.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('data-product-info')
    elem_data = json.loads(data)
    name = elem_data['productName']
    id = elem_data['productId']
    price = elem_data['productPriceLocal']
    link = product.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('href')
    elem['name'] = name
    elem['_id'] = id
    elem['price'] = price
    elem['link'] = link
    list.append(elem)
    mvideo.insert_one({'_id': id, 'name': name, 'price': price, 'link': link})

for elem in mvideo.find({}):
    print(elem)