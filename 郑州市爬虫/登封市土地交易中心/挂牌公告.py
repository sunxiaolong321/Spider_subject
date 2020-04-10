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
            time.sleep(random.randint(0, 2))
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
        data = pd.read_html(msgs.prettify())[0]
        columns = [s.replace(' ', '').replace('\n', '')
                        for s in data.iloc[1:2].to_numpy().tolist()[0]]
        for index in range(len(columns)):
            if columns[index].startswith('土地面积'):
                columns[index] = ('土地面积')
            if columns[index].startswith('挂牌起始价'):
                columns[index] = ('挂牌起始价')
        data.columns = columns
        data = data[2:]
        li = []
        for dic in list(data.T.to_dict().values())[2:]:
            result = {
                '编号': dic['编号'].replace(' ', '').replace('\n', ''),
                '宗地位置': dic['土地位置'].replace(' ', '').replace('\n', ''),
                '地块面积（平方米）': dic['土地面积'].replace(' ', '').replace('\n', ''),
                '用途': dic['土地用途'].replace(' ', '').replace('\n', ''),
                '容积率': dic['容积率'].replace(' ', '').replace('\n', ''),
                '限高': dic['建筑高度（米）'].replace(' ', '').replace('\n', ''),
                '出让年限': dic['出让年限（年）'].replace(' ', '').replace('\n', ''),
                '起始价格（万元）': dic['挂牌起始价'].replace(' ', '').replace('\n', ''),
            }
            li.append(result)
        return li
    except Exception as e:
        print(data.columns)
        raise e


# 解析详情页
if __name__ == "__main__":
    li = []
    count = 1
    result = pd.DataFrame()
    for page in range(1, 3):
        print('正在抓取第 %d 页' % page)
        html = resReq(
            'http://www.dfggzyjy.com/jyxx/005005/005005001/%d.html' % page)
        urlLi = parseHtml(html)
        for url in urlLi:
            try:
                print('正在抓取第 %d 条信息' % count)
                count += 1
                url = 'http://www.dfggzyjy.com'+url
                html = resReq(url)
                result = getDetail(html)
                li += result
            except Exception as e:
                print(e)
                with open('error.txt','a') as f:
                    f.write(url+'\n')
    # print(parseHtml(html))
    pd.DataFrame(li).to_csv('登封市公共资源交易中心-挂牌公告.csv', encoding='utf-8')
