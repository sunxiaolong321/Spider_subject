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
    urls = soup.findAll(class_='wb-data-infor')
    li = []
    for url in urls:
        li.append(url.a.get('href'))
    return li


def getDetail(html):

    soup = BeautifulSoup(html, 'lxml')
    try:
        msgs = soup.select_one('table')
        li = []
        table = pd.read_html(msgs.prettify())[0]
        columns = [s.replace(' ', '').replace('\n', '')
                   for s in table.iloc[0:1].to_numpy().tolist()[0]]
        table.columns = columns
        li = []
        for dic in list(table.T.to_dict().values())[1:]:
            try:
                result = {
                    '地块编号': dic['地块编号'].replace(' ', '').replace('\n', ''),
                    '宗地位置': dic['位置'].replace(' ', '').replace('\n', ''),
                    '地块面积（平方米）': dic['土地面积（平方米）'].replace(' ', '').replace('\n', ''),
                    '用途': dic['土地用途'].replace(' ', '').replace('\n', ''),
                    '成交价格（万元）': dic['成交价（万元）'].replace(' ', '').replace('\n', ''),
                    '受让单位': dic['竞得人'].replace(' ', '').replace('\n', ''),
                    '成交时间': soup.select_one('body > div.ewb-container.ewb-alter.ewb-article.clearfix > div.ewb-about-content > div > p:nth-child(7)').get_text()
                }
            except:
                result = {
                    '地块编号': dic['地块编号'].replace(' ', '').replace('\n', ''),
                    '宗地位置': dic['位置'].replace(' ', '').replace('\n', ''),
                    '地块面积（平方米）': dic['使用权面积（平方米）'].replace(' ', '').replace('\n', ''),
                    '用途': dic['土地用途'].replace(' ', '').replace('\n', ''),
                    '成交价格（万元）': dic['成交价（万元）'].replace(' ', '').replace('\n', ''),
                    '受让单位': dic['竞得人'].replace(' ', '').replace('\n', ''),
                    '成交时间': soup.select_one('body > div.ewb-container.ewb-alter.ewb-article.clearfix > div.ewb-about-content > div > p:nth-child(6)').get_text()+soup.select_one('body > div.ewb-container.ewb-alter.ewb-article.clearfix > div.ewb-about-content > div > p:nth-child(7)').get_text()
                }
            li.append(result)
        return li
    except Exception as e:
        print(e)
        raise e
    return li


# 解析详情页
if __name__ == "__main__":
    li = []
    count = 1
    for page in range(1, 2):
        print('正在抓取第%d页'%page)
        html = resReq(
            'http://www.zmxggzy.com/jyxx/003004/003004003/secondPage.html')
        urlLi = parseHtml(html)
        for url in urlLi:
            try:
                print('正在抓取第%d条信息'%count)
                count += 1
                url = 'http://www.zmxggzy.com'+url
                html = resReq(url)
                result = getDetail(html)
                li += result
            except:
                with open('error.txt','a') as f:
                    f.write(url+'\n')
    # print(parseHtml(html))
    pd.DataFrame(li).to_csv('中牟县公共资源交易中心-结果公告_1.csv', encoding='utf-8')
