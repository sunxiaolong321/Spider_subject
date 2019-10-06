# 去哪儿网景点信息爬取|Scrapy for qunaer

## 简介

Scrapy框架爬取去哪儿景点信息保存到MySQL数据库

## 需求库

- Scrapy
- twisted
- pymysql
- urllib
- fake_useragent

## 运行

    scrapy crawl qunar

项目使用一个老哥的Redis代理项目使用代理爬取

## 保存参数

参数|含义|示例|类型
---|---|---|---
title|景点名称|八达岭长城|string
city|城市|北京市|string
place|北京北京|string
hot|热度评分|0.82|string
level|景点评级|5A景区|string
site|详细地址|地址：北京市延庆县军都山关沟古道北口216省道附近|string
note|网站评价|不到长城非好汉|string
price|价格|40|float
sale|销量|16382|int

[Redis代理项目地址](https://github.com/jhao104/proxy_pool)
