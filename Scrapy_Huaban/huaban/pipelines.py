# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class HuabanPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        url = request.url
        type = request.meta['type']
        file_name = url.split('/')[-1]+'.'+type
        return file_name

    def get_media_requests(self, item, info):
        data = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
        }
        yield Request(item['url'], headers=data, meta={'type': item['type']})

