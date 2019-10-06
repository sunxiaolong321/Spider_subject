# -*- coding: utf-8 -*-
import json
import time

import requests
import scrapy
from scrapy import Request


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['kuaidaili.com/free/']

    def start_requests(self):
        headers = {
            'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': ' gzip, deflate, br',
            'Accept-Language': ' zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': ' max-age=0',
            'Connection': ' keep-alive',
            'Cookie': ' channelid=0; sid=1552009298654176; _ga=GA1.2.1439074236.1552009301; _gid=GA1.2.716091973.1552009301; _gat=1',
            'DNT': ' 1',
            'Host': ' www.kuaidaili.com',
            'Referer': ' https://www.kuaidaili.com/free/',
            'Upgrade-Insecure-Requests': ' 1',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
        for i in range(1, 10):
            time.sleep(1)
            yield Request('https://www.kuaidaili.com/free/intr/%s/' % i, headers=headers)

    def parse(self, response):
        for sel in response.xpath('//table/tbody/tr[position()>=1]'):
            ip = sel.css('td:nth-child(1)::text').extract_first()
            port = sel.css('td:nth-child(2)::text').extract_first()
            httptype = sel.css('td:nth-child(4)::text').extract_first().lower()
            url = '%s://httpbin.org/ip' % httptype
            proxy = '%s://%s:%s' % (httptype, ip, port)
            print(proxy)
            if self.ipUtils(proxy):
                yield {
                    'ip': url,
                    'httptype': httptype
                }

    def ipUtils(self, proxy):
        # 设置代理头
        proxies = {'http': proxy}
        print('正在测试：{}'.format(proxies))
        try:
            r = requests.get('http://www.baidu.com', proxies=proxies, timeout=3)
            if r.status_code == 200:
                print('该代理：{}成功存活'.format(proxy))
                return True
        except:
            print('该代理{}失效！'.format(proxies))
            return False
