#Урок 3

#Задание 1.
# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД.

import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import re
from pymongo import MongoClient

#https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA&page=1

main_link = 'https://hh.ru/search/vacancy'

vacancy = 'грумер'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}

page_num = 0

vacancies = []

while True:
    params = {
        'L_is_autosearch':'false',
        'clusters': 'true',
        'enable_snippets': 'true',
        'text': vacancy,
        'page': page_num
        }

    response = requests.get(main_link, params=params, headers=headers)

    dom = bs(response.text, 'html.parser')

    vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    for vacancy in vacancy_list:
        vacancy_data = {}

        vacancy_name = vacancy.find('a').text

        vacancy_link = vacancy.find('a')['href']

        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.getText().replace('\xa0', '')
            salary = re.split(' |-', salary)

            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1])
                salary_currency = salary[2]
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = None
                salary_currency = salary[2]
            else:
                salary_min = int(salary[0])
                try:
                    salary_max = int(salary[1])
                except ValueError:
                    salary_max = None
                salary_currency = salary[2]

            regex_num = re.compile('\d+')
            s = regex_num.search(vacancy_link)
            vacancy_id = vacancy_link[s.start():s.end()]

            vacancy_data['_id'] = int(vacancy_id)
            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency
            vacancy_data['web site'] = 'https://hh.ru/'

            vacancies.append(vacancy_data)


    if dom.find(text='дальше'):
        page_num += 1
    else:
        break
pprint(vacancies)
# Задание 2
# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

import numpy as pd
import pandas as pd
df = pd.DataFrame(vacancies)

client = MongoClient('127.0.0.1', 27017)
db = client['hhru']
vacancies_hh = db.vacancies_hh

vacancies_hh.insert_many(vacancies)

max_salary = int(input('Введите максимальную заработную плату:'))

for vacancy in vacancies_hh.find({'$or': [{'salary_max': {'$gt': max_salary}}, {'salary_min': {'$gt': max_salary}}]}):
    pprint(vacancy)

# Задание 3
# Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
new_vacancies_number = 0
for vacancy_check in vacancies:
    vacancy_check_count = vacancies_hh.count_documents({'_id': vacancy_check['_id']})
    if vacancy_check_count == 0:
        vacancies_hh.insert_one({'_id': vacancy_check['_id'], 'currency': vacancy_check['currency'], 'name': vacancy_check['name'], 'salary_max': vacancy_check['salary_max'],
        'salary_min': vacancy_check['salary_min'], 'vacancy_link': vacancy_check['vacancy_link']})
        new_vacancies_number += 1

print('Добавлено %i новых вакансий' % (new_vacancies_number))