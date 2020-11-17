#Урок 2
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#* Наименование вакансии.
#* Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
#* Ссылку на саму вакансию.
#* Сайт, откуда собрана вакансия.

#По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.

import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import re

#https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=Data+scientist&from=suggest_post

main_link = 'https://hh.ru'

vacancy = input('Введите интересующую вакансию: ')

params = {'clusters': 'true',
          'enable_snippets': 'true',
          'salary': '',
          'st': 'searchVacancy',
          'text': vacancy
          }

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}

result = requests.get(main_link + '/search/vacancy', params=params, headers=headers)

dom = bs(result.text, 'html.parser')

page_block = dom.find('div', {'data-qa': 'pager-block'})
if not page_block:
    last_page = 1
else:
    last_page = int(page_block.find_all('a', {'class': 'HH-Pager-Control'})[-2].getText())
    print(f'last page {last_page}')

for page in range(0, last_page):
    params['page'] = page
    result = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
    dom = bs(result.text, 'html.parser')

    vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

    vacancies = []
    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_elem = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})
        vacancy_name = vacancy_elem.getText()

        vacancy_link = vacancy_elem['href']

        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            salaty_currency = None
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

        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency
        vacancy_data['web site'] = 'https://hh.ru/'

        vacancies.append(vacancy_data)

pprint(vacancies)