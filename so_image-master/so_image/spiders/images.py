# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy import Request
import json
from so_image.items import ImageItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['image.so.com']

    def start_requests(self):
        data = {
            'ch': 'beauty',
            'listtype': 'new',
            'temp': '1'
        }
        base_url = 'http://images.so.com/zj?'
        for page in range(1, self.settings.get('MAX_PAGE')+1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url+params
            yield Request(url, self.images_url)

    def images_url(self, response):
        result = json.loads(response.text)
        data = {
            'ch': 'beauty'
        }
        base_url = 'http://images.so.com/zvj?'
        for items in result.get('list'):
            id = items.get('id')
            data['id'] = id
            images_url = base_url+urlencode(data)
            yield Request(images_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print(response)
        result = json.loads(response.text)
        for items in result.get('list'):
            item = ImageItem()
            item['url'] = items.get('qhimg_url')
            yield item
