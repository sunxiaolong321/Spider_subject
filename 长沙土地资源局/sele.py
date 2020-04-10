import requests
from bs4 import BeautifulSoup
import re
import time
import random
import pandas as pd


def get_msg(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Cookie': 'JSESSIONID=grPt-RsHssO7V6nOU8Qtb9yoU74M8MTECu3EwR-G7xlf_KVD3rgR!-243266402',
    }
    r = requests.get(url, headers=headers, timeout=5)
    time.sleep(random.randint(0, 2))
    r.encoding = 'gbk'
    if r.ok:
        return r.text


def parse_index_html(html):
    soup = BeautifulSoup(html, 'lxml')
    parent = soup.find(name='table', class_='xxtable2')
    li = []
    for children in parent.findAll('tr')[:15]:
        result = {'id': None, '交易状态': None}
        id = children.select_one('tr > td:nth-child(1) > a')['href']
        # print(id)
        try:
            result['id'] = re.match(r"javascript:goRes[(]'(\d+)','01'[)];", id)[1]
        except:
            continue
        result['交易状态'] = children.select_one('tr > td:nth-child(4)').text
        li.append(result)
    return li

# 详情页信息 已经成交


def parse_html_deal(html):
    soup = BeautifulSoup(html, features="lxml")
    result = {
        "行政区": None,
        '编号': None,
        '区县': None,
        "宗地名称": None,
        "宗地位置": None,
        "面积（平方米）": None,
        "用途": None,
        "交易方式": None,
        "出让年限": None,
        "起始价格（万元）": None,
        "成交价格（万元）": None,
        "受让单位": None,
        "容积率": None,
        "交易时间": None,
        '其他': None,
        '成交状态': None,
        'id': None,
    }
    parent = soup.find(class_='td_line2').table
    # print(parent)
    result['行政区'] = '长沙市'
    result['编号'] = parent.select_one('tr:nth-child(1) > td:nth-child(2)').text
    result['区县'] = parent.select_one(
        'tr:nth-child(6) > td:nth-child(2)').text.strip()
    result['宗地位置'] = parent.select_one(
        'tr:nth-child(5) > td:nth-child(2)').text.strip()
    result['面积（平方米）'] = parent.select_one(
        'tr:nth-child(6) > td:nth-child(4)').text.strip()
    result['用途'] = parent.select_one(
        'tr:nth-child(7) > td:nth-child(4)').text.strip()
    result['交易方式'] = '挂牌'
    result['出让年限'] = parent.select_one(
        'tr:nth-child(8) > td:nth-child(2)').text.strip()
    result['起始价格（万元）'] = parent.select_one(
        'tr:nth-child(8) > td:nth-child(4)').text.strip()
    result['成交价格（万元）'] = parent.select_one(
        'tr:nth-child(13) > td:nth-child(2)').text.strip().replace('\n', '').replace('\r', '').replace('\t', '')
    result['受让单位'] = parent.select_one(
        'tr:nth-child(13) > td:nth-child(4)').text.strip().replace('\n', '').replace('\r', '')
    result['容积率'] = parent.select_one(
        'tr:nth-child(7) > td:nth-child(2)').text.strip()
    result['交易时间'] = parent.select_one(
        'td:nth-child(11)').text
    result['其他'] = parent.select_one(
        'tr:nth-child(12) > td:nth-child(2)').text
    return result


# 详情页信息 终止
def parse_html_undeal(html):
    soup = BeautifulSoup(html, 'lxml')
    result = {
        "行政区": None,
        '编号': None,
        '区县': None,
        "宗地名称": None,
        "宗地位置": None,
        "面积（平方米）": None,
        "用途": None,
        "交易方式": None,
        "出让年限": None,
        "起始价格（万元）": None,
        "成交价格（万元）": None,
        "受让单位": None,
        "容积率": None,
        "交易时间": None,
        '其他': None,
        '成交状态': None,
        'id': None,
    }
    parent = soup.find(class_='td_line2').table
    result['行政区'] = '长沙市'
    result['编号'] = parent.select_one('tr:nth-child(1) > td:nth-child(2)').text
    result['区县'] = parent.select_one(
        'tr:nth-child(6) > td:nth-child(2)').text.strip()
    result['宗地位置'] = parent.select_one(
        'tr:nth-child(5) > td:nth-child(2)').text.strip()
    result['面积（平方米）'] = parent.select_one(
        'tr:nth-child(6) > td:nth-child(4)').text.strip()
    result['用途'] = parent.select_one(
        'tr:nth-child(7) > td:nth-child(4)').text.strip()
    result['交易方式'] = '挂牌'
    result['出让年限'] = parent.select_one(
        'tr:nth-child(8) > td:nth-child(2)').text.strip()
    result['起始价格（万元）'] = parent.select_one(
        'tr:nth-child(8) > td:nth-child(4)').text.strip()
    # result['成交价格（万元）'] = parent.select_one(
    #     'tr:nth-child(13) > td:nth-child(2)').text.strip().replace('\n', '').replace('\r', '').replace('\t', '')
    # result['受让单位'] = parent.select_one(
    #     'tr:nth-child(13) > td:nth-child(4)').text.strip().replace('\n', '').replace('\r', '')
    result['容积率'] = parent.select_one(
        'tr:nth-child(7) > td:nth-child(2)').text.strip()
    # result['交易时间'] = parent.select_one(
    #     'td:nth-child(11)').text
    result['其他'] = parent.select_one(
        'tr:nth-child(10) > td:nth-child(2)').text.strip()
    return result


if __name__ == "__main__":
    count = 1
    for page in range(53, 71):
        print('正在抓取第 %d 页' % page)
        index_url = 'http://gtzy.csggzy.cn/deala_js_action_gg_jg?resourcelb=06&SSXZQ=&currentPage=%d' % page
        html = get_msg(index_url)
        li = []
        for msg in parse_index_html(html):
            print('正在抓取第 %d 条信息' % count)
            count += 1
            detail_url = 'http://gtzy.csggzy.cn/landinfo?ResourceID=%s' % msg['id']
            html = get_msg(detail_url)
            if msg['交易状态'] == '成交':
                result = parse_html_deal(html)
            else:
                result = parse_html_undeal(html)
            result['成交状态'] = msg['交易状态']
            result['id'] = msg['id']
            li.append(result)
        pd.DataFrame(li).to_excel('./data/%d.xlsx' % page)
    print('全部保存成功')
