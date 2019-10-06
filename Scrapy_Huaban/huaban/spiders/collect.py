# -*- coding: utf-8 -*-
import json
import re
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from huaban.huaban.items import HuabanItem


class CollectSpider(scrapy.Spider):
    name = 'collect'
    allowed_domains = ['huaban.com']

    def start_requests(self):
        base_url = 'https://huaban.com/search/?'
        data = {
            'q': 'girl',
            'jsvap91g': '',
            'page': '',
            'per_page': '20',
            'wfl': '1'
        }
        for page in range(1, 10):
            data['page'] = page
            params = urlencode(data)
            url = base_url + params
            headers = {
                'Host': 'huaban.com',
                'Connection': 'keep-alive',
                'Accept': 'application/json',
                'DNT': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Request': 'JSON',
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
                'Referer': 'http://huaban.com/search/?q=girl',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cookie': 'sid=rPdc2BOx36u9oWbBakDdrjOEsnN.R3HLWOCdqqemTpMp0TfU26GHQE0QZ%2FEHw3ksmtWGuf8; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2uhgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1366.768.24; _uab_collina=155176134686883515072549; _hmt=1',
            }
            yield Request(url, self.parse, headers=headers)

    def parse(self, response):
        result = json.loads(response.text)
        base_url = 'http://img.hb.aicdn.com/'
        res = result.get('pins')
        for ret in res:
            num = ret['file']['key']
            type = re.search('/(\w+)', ret['file']['type'], flags=0).group(1)
            item = HuabanItem()
            item['url'] = base_url + num
            item['type'] = type
            yield item
