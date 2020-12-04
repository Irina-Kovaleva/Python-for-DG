import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroySpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response:HtmlResponse):
        goods_links = response.xpath("//a[@class='plp-item__info__title']")
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return



    def parse_good(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//uc-pdp-price-view[@class='primary-price']//span[@slot='price']/text()")
        loader.add_xpath('unit', "//uc-pdp-price-view[@class='primary-price']//span[@slot='unit']/text()")
        loader.add_xpath('char_name', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('char_value', "//dd[@class='def-list__definition']/text()")
        loader.add_value('characteristics', {})
        yield loader.load_item()