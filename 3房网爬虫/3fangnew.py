import csv
import json
import os
import pickle
import time
from random import randint

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests import Session


class Fang:
    def __init__(self):
        self.session = Session()

    def get_cookies(self, count):
        with open('cookie.json', 'r') as f:
            cookie = json.load(f)
            return cookie['cookies%d' % count]

    def doLogin(self, phoneNumber):
        # 模拟登陆
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
            "Referer": "http://passport.3fang.com/"
        }
        data = {
            'MobilePhone': phoneNumber,
            'Operatetype': 0,
            'Service': 'soufun-3fang-web',
        }
        self.session.get('http://passport.3fang.com/', headers=headers)
        self.session.post('http://passport.3fang.com/loginsendmsm.api',
                          headers=headers, data=data)
        mobileCode = eval(input('验证码： '))
        params = {
            'mobilephone': phoneNumber,
            'mobilecode': mobileCode,
            'operatetype': 0,
            'service': 'soufun-3fang-web',
        }
        r = self.session.get(
            'http://passport.3fang.com/loginverifysms.api', headers=headers, params=params)
        if r.json()["Message"] == "Success":
            print("注册成功")

    def cookieLogin(self, count):
        with open('./cookies/cookie%d' % count, 'rb') as f:
            self.session.cookies.update(pickle.load(f))

    def get_detail(self, url, cookiesItem=1, flag=False):
        count = 5
        while count >= 0:
            try:
                response = self.session.get(url, timeout=10)
                response.encoding = 'gbk'
                return response.text
            except Exception as e:
                print(e)
                if count <= 0:
                    return ""
                print("正在重试")
                count -= 1

    def parse_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        delist = []
        for detail in soup.select("#landlb_B04_22 > dd"):
            result = {
                "县区": None,
                "url": None,
            }
            result["url"] = detail.find("a").get("href")
            result["县区"] = detail.select(
                "div.list28_text.fl > table > tbody > tr:nth-child(2) > td:nth-child(4)")[0].get_text()
            delist.append(result)
        return delist

    def parse_detail_html(self, html):
        result = {
            "用途": None,
            "宗地名称": None,
            "省市": None,
            "区县": None,
            "地块公告号": None,
            "宗地位置": None,
            "出让年限": None,
            "交易方式": None,
            "起始价（万元）": None,
            "成交价（万元）": None,
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
        try:
            soup = BeautifulSoup(html, "lxml")
            result["用途"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(8) > td:nth-child(2) > a")[0].get_text()
            result['区县'] = soup.select(
                '#wrapper > div.crumbs > a:nth-child(6)')[0].get_text()
            result["宗地名称"] = soup.find(class_="tit_box01").get_text()
            result["省市"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(1) > td:nth-child(1) > a")[0].get_text()
            result["地块公告号"] = soup.select("#printData1 > div.menubox01.mt20 > span")[
                0].get_text()[5:]
            result["宗地位置"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(7) > td:nth-child(2)")[0].get_text()[3:]
            result["出让年限"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(7) > td:nth-child(1)")[0].get_text()[5:]
            result["交易方式"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(6) > td:nth-child(2)")[0].get_text()[5:]
            result["起始价（万元）"] = soup.select(
                "#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(4) > td:nth-child(1)")[0].get_text()[4:]
            result["成交价（万元）"] = soup.select(
                "#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(4) > td:nth-child(2)")[0].get_text()[4:]
            result["溢价率"] = soup.select(
                "#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(5) > td:nth-child(2)")[0].get_text()[4:]
            result["成交时间"] = soup.select(
                "#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(3) > td:nth-child(1)")[0].get_text()[5:]
            result["地块面积（平方米）"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(2) > td:nth-child(1) > em")[0].get_text()
            result["容积率"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(4) > td:nth-child(1)")[0].get_text()[4:]
            result["建筑面积（平方米）"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(3) > td:nth-child(1) > em")[0].get_text()
            result["限高（米）"] = soup.select(
                "#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(6) > td:nth-child(1)")[0].get_text()[5:]
            result["受让单位"] = soup.select(
                "#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(1) > td:nth-child(2)")[0].get_text()[4:]
            result['交易状况'] = soup.select(
                '#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(1) > td:nth-child(1)')[0].get_text()[5:]
        except Exception as e:
            print(e)
            return result
        return result

    def get_detail_url(self, url):
        html = self.get_detail(url)
        index_msg = self.parse_html(html)
        return_data = []
        for detail_msg in index_msg:
            tmp_dic = {}
            tmp_dic['url'] = 'https://land.3fang.com'+detail_msg['url']
            tmp_dic['区县'] = detail_msg['县区']
            return_data.append(tmp_dic)
        return return_data

    def get_info(self, urls, cookieCount=1):
        count = 1
        sum_html = []
        # 获取详情页信息
        start = time.perf_counter()
        for url in urls:
            print("正在抓取第 %d 条信息" % count)
            count += 1
            tmp = {'url': url, 'html': None}
            tmp['html'] = self.get_detail(url, cookieCount, flag=True)
            sum_html.append(tmp)
        end = time.perf_counter()

        return_data = []
        count = 1
        for detail in sum_html:
            print('正在解析第 %d 条信息' % count)
            count += 1
            result = self.parse_detail_html(detail['html'])
            result['url'] = detail['url']
            return_data.append(result)
        return return_data

    def saveLocation(self):
        count = 1
        flag = True
        while flag:
            filelist = os.listdir('./cookies')
            filename = "cookie%s" % count
            if filename in filelist:
                count += 1
            else:
                flag = False
        with open("./cookies/%s" % filename, "wb") as f:
            pickle.dump(self.session.cookies, f)

        # if __name__ == "__main__":
        #     session = Fang()
        #     for page in range(1, 2):
        #         data = session.get_info(
        #             'https://land.3fang.com/market/410100__1______3_0_%d.html' % page)
        #         with open('./data/住宅用地.csv', 'a',newline='', encoding='gbk') as f:
        #             csv_writer = csv.writer(f)
        #             csv_writer.writerow(list(data[0].keys()))
        #             for d in data:
        #                 try:
        #                     csv_writer.writerow(list(d.values()))
        #                 except:
        #                     print('保存失败')
        #                     with open('error.text', 'a', encoding='gbk') as f1:
        #                         f1.write(d['url']+'\n')
        # print('全部保存成功')
        # if __name__ == "__main__":
        #     session = Fang()
        #     detail_urls = []
        #     for page in range(1, 3):
        #         print('正在解析第 %d 页' % page)
        #         detail_urls += session.get_detail_url(
        #             'https://land.3fang.com/market/410100__4______2_0_%d.html' % page)
        #         session.get_info(detail_urls)


if __name__ == "__main__":
    session = Fang()
    mode = input('登陆 或 注册： ')
    if mode == "注册":
        phoneNumber = eval(input('手机号码：'))
        session.doLogin(phoneNumber)
        session.saveLocation()
    else:
        count = eval(input('输入cookie条目： '))
        session.cookieLogin(count)
    data = pd.read_csv('./urls/住宅用地-已成交-挂牌.csv')
    urls = data['url'].tolist()
    itemstart = eval(input('输入条数: '))
    print('项目共有 %d 条' % len(urls))
    if len(urls)-itemstart < 100:
        itemend = len(urls)
    else:
        itemend = itemstart+100
    result = session.get_info(urls[itemstart:itemend])
    with open('./data/补充.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(result[0].keys()))
        if itemstart == 0:
            writer.writeheader()
        writer.writerows(result)
