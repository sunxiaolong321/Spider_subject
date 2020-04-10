import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

def resReq(url):
    # 解析链接
    count = 5
    while count:
        try:
            time.sleep(random.randint(1, 3))
            r = requests.get(url)
            if r.ok:
                return r.text
        except:
            print('抓取失败，正在重试')
            count -= 1
    return ""


def parseHtml(html):
    # 解析首页
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.findAll(class_='ewb-com-block l')
    li = []
    for url in urls:
        li.append(url.a.get('href'))
    return li


def getDetail(html):

    soup = BeautifulSoup(html, 'lxml')
    msgs = soup.select('table > tbody > tr')
    li = []
    for msg in msgs[1:]:
        result = {
            '地块编号': None,
            '宗地位置': None,
            '地块面积（平方米）': None,
            '用途': None,
            '成交价格（万元）': None,
            '受让单位': None,
        }
        child = list(msg.findAll('td'))
        result['地块编号'] = child[1].get_text().replace('\n', '').strip()
        result['宗地位置'] = child[2].get_text().replace('\n', '').strip()
        result['地块面积（平方米）'] = child[3].get_text().replace('\n', '').strip()
        result['用途'] = child[4].get_text().replace('\n', '').strip()
        result['成交价格（万元）'] = child[5].get_text().replace('\n', '').strip()
        result['受让单位'] = child[6].get_text().replace('\n', '').strip()
        li.append(result)
    return li


# 解析详情页
if __name__ == "__main__":
    li = []
    count = 1
    for page in range(1, 11):
        print('正在抓取第%d页'%page)
        html = resReq('http://www.zzsggzy.com/gtzy/006003/%d.html' % page)
        urlLi = parseHtml(html)
        for url in urlLi:
            print('正在抓取第%d条信息'%count)
            count += 1
            url = 'http://www.zzsggzy.com/'+url
            html = resReq(url)
            result = getDetail(html)
            li += result
    # print(parseHtml(html))
    pd.DataFrame(li).to_csv('郑州公共资源交易中心-结果公告.csv', encoding='utf-8')
