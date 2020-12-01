# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        if spider.name == 'hhru':
            item['salary'] = self.salary_processing_hh(item['salary'])
            vacancy_name = item['name']
            vacancy_link = item['link']
            salary_min = item['salary'][0]
            salary_max = item['salary'][1]
            salary_currency = item['salary'][2]
            vacancy_website = item['source']
            vacancy = {
                'vacancy_name': vacancy_name,
                'vacancy_link': vacancy_link,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'salary_currency': salary_currency,
                'vacancy_website': vacancy_website
            }
        elif spider.name == 'sjru':
            item['salary'] = self.salary_processing_sjru(item['salary'])
            vacancy_name = ''.join(item['name'])
            vacancy_link = item['link']
            salary_min = item['salary'][0]
            salary_max = item['salary'][1]
            salary_currency = item['salary'][2]
            vacancy_website = item['source']
            vacancy = {
                'vacancy_name': vacancy_name,
                'vacancy_link': vacancy_link,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'salary_currency': salary_currency,
                'vacancy_website': vacancy_website
            }


        collection.insert_one(vacancy)
        return item

    def salary_processing_hh(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None
        for i in range(len(salary)):
            salary[i] = salary[i].replace('\xa0', '')

        if salary[0] == 'до' and len(salary) == 5:
            salary_max = float(salary[1])
            salary_currency = salary[3]
        elif salary[0] == 'от' and len(salary) == 5:
            salary_min = float(salary[1])
            salary_currency = salary[3]
        elif len(salary) == 7:
            salary_min = float(salary[1])
            salary_max = float(salary[3])
            salary_currency = salary[5]

        list_salary = [salary_min, salary_max, salary_currency]
        return list_salary


    def salary_processing_sjru(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None
        for i in range(len(salary)):
            salary[i] = salary[i].replace('\xa0', '')

        if salary[0] == 'до':
            salary_currency = salary[2][-4:]
            salary_max = float(salary[2].replace('руб.', ''))

        elif salary[0] == 'от':
            salary_currency = salary[2][-4:]
            salary_min = float(salary[2].replace('руб.', ''))

        elif len(salary) == 7:
            salary_min = float(salary[0])
            salary_max = float(salary[4])
            salary_currency = salary[6]


        list_salary = [salary_min, salary_max, salary_currency]
        return list_salary
