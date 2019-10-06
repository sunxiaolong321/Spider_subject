# 拉勾网求职信息爬取

## 项目简述

拉勾网简单爬虫，按照请求构造方式的不同请求不同条件的信息进行筛选以及后期的数据处理

## Requestments

- fake-useragent == 0.1.11
- requests == 2.22.0
- python >= 3.6

## 选项设置

### 在`settings.py`里直接选择构造方式

目前没有对项目进行包装优化，仅达到了能用阶段
构造方式详见settings.py

### `parsedata.py`为解析链接，还未完善

解析json格式文本，进行数据整理和清洗

### `main.py`主程序入口

main.py 为主程序入口。进入程序目录，命令行运行`python main.py`

### `savedata.py`构造data保存方式（暂未完善）

可选项为mysql，mongodb
settings中1表示mysql，2表示mongodb

## 实现思路

### 拉勾网的反爬措施

我们所需请求信息保存在position中，为一个post请求。请求头构造中需要加入一个cookies和referer，缺失将导致请求频繁的错误。

解决这一问题的方法是维持一个请求对话，从请求链接中获取指定cookies，并且在position请求头中加入referer，referer与请求链接相同。

## 程序功能

按照给定关键词和限制条件查询数据
可以选择的关键词为页数，地区、薪资、工作经验、是否为校招、实习生等
具体限制条件和关键词可在settings.py中查看