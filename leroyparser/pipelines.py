# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient



class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['characteristics'] = dict(zip(item['char_name'], item['char_value']))
        collection.insert_one(item)
        return item

class OTPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        dir = item['name']
        image_guid = request.url.split('/')[-1]
        return f'{dir}/img{image_guid}'

