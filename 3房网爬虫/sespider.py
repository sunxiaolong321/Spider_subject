import json
import os
import time
import random

import pandas as pd
from selenium import webdriver
import csv
options = webdriver.ChromeOptions()
options.add_argument("--ignore-ssl-errors")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-certificate-errors-spki-list")
browser = webdriver.Chrome(options=options)
browser.get('https://www1.3fang.com/')
browser.delete_all_cookies()
browser.maximize_window()
with open('cookies_csnd2.json', 'r', encoding='utf-8') as f:
    list_cookies = json.load(f)
print(list_cookies)

# 添加cookie到selenium
for i in list_cookies:
    if i.get('expiry'):
        i.pop('expiry')
    browser.add_cookie(i)

# 模仿cookie
# time.sleep(100)
# cookies = browser.get_cookies()
# json_cookies = json.dumps(cookies)
# with open('cookies_csnd2.json', 'w') as f:
#     f.write(json_cookies)

file = './urls/工业用地.xlsx'
result_list = []
for index, row in pd.read_excel(file, index_col=0)[118:150].iterrows():
    url = row[0]
    city = row[1]
    tmp = random.randint(2, 6)
    print('暂停 %d 秒' % tmp)
    time.sleep(tmp)
    print('正在抓取第 %d 条信息' % index)
    browser.get(url)
    # js = 'var action=document.documentElement.scrollTop=10000'
    # browser.execute_script(js)
    result = {
        "规划用途": None,
        "宗地名称": None,
        "省市": None,
        "区县": None,
        "地块公告号": None,
        "宗地位置": None,
        "出让年限": None,
        "交易方式": None,
        "起始价格（万元）": None,
        "成交价格（万元）": None,
        "溢价率": None,
        "成交时间": None,
        "地块面积（平方米）": None,
        "容积率": None,
        "建筑面积（平方米）": None,
        "限高（米）": None,
        "受让单位": None,
        '交易状况': None,
        'url': None,

    }
    result['区县'] = city
    result['url'] = url
    try:
        result['宗地名称'] = browser.find_element_by_class_name(
            'tit_box01').text.strip()
        result['地块公告号'] = browser.find_element_by_css_selector(
            '#printData1 > div.menubox01.mt20 > span').text.strip()[5:]
        result['地块面积（平方米）'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(2) > td:nth-child(1) > em').text.strip()
        result['宗地位置'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(7) > td:nth-child(2)').text.strip()[3:]
        result['规划用途'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(8) > td:nth-child(2) > a').text
        result['交易方式'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(6) > td:nth-child(2)').text.strip()[5:]
        result['容积率'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(4) > td:nth-child(1)').text.strip()[4:]
        result['限高（米）'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(6) > td:nth-child(1)').text.strip()[5:]
        result['出让年限'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(7) > td:nth-child(1)').text.strip()[5:]
        result['出让年限'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(7) > td:nth-child(1)').text.strip()[5:]
        result['出让年限'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(7) > td:nth-child(1)').text.strip()[5:]
        result['起始价格（万元）'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(4) > td:nth-child(1)').text.strip()[4:]
        result['成交价格（万元）'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()[4:]
        result['溢价率'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(5) > td:nth-child(2)').text.strip()[4:]
        result['成交时间'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(3) > td:nth-child(1)').text.strip()[5:]
        result['建筑面积（平方米）'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(3) > td:nth-child(1) > em').text.strip()
        result['受让单位'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(1) > td:nth-child(2)').text.strip()[4:]
        result['交易状况'] = browser.find_element_by_css_selector(
            '#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(1) > td:nth-child(1)').text.strip()[5:]
    except:
        pass
    result_list.append(result)
browser.close()
    # pd.DataFrame(result_list).to_excel('./data/'+fileName)
with open('./data/工业用地.csv','a', encoding='gbk',newline='') as f:
    witer = csv.writer(f)
    # witer.writerow(result_list[0].keys())
    witer.writerows(d.values() for d in result_list[1:])