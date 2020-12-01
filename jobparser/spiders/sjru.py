import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python%20developer&geo%5Bt%5D%5B0%5D=4']


    def parse(self, response:HtmlResponse):
        vacancies_links = response.xpath("//div/a[contains(@class, 'icMQ_ _6AfZ9 f-test-link')]/@href").extract()
        for link in vacancies_links:
             yield response.follow(link, callback=self.vacansy_parse)
        next_page = response.xpath("//a[contains(@class, 'f-test-link-Dalshe')]/@href").extract_first()
        if next_page:
             yield response.follow(next_page, callback=self.parse)
        else:
            return


    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']//text()").extract()
        vacancy_link = response.url
        vacancy_source = 'superjob.ru'
        yield JobparserItem(name=name, salary=salary, link=vacancy_link, source=vacancy_source)