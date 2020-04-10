import requests
from bs4 import BeautifulSoup
from requests import Session
from fontTools.ttLib import TTFont
import execjs
import re
import pandas as pd
import copy
def resUrl(url, mode=1):
    flag = 5
    while flag:
        try:
            res = requests.get(url)
            if res.ok:
                # res.encoding = 'gbk'
                print('程序抓取成功')
                if mode == 2:
                    return res.content
                return res.text
            res -= 1
            print('抓取失败，正在重试')
        except Exception as e:
            res -= 1
            print('抓取发生错误\n%s' % e)


def parseHtml(htm):
    soup = BeautifulSoup(htm, 'lxml')
    result = soup.findAll(class_='title-link')
    li = []
    for detail in result:
        li.append(detail.get('href'))
    return li


class resSession():
    def __init__(self):
        self.session = Session()
        self.resultData = {
            "省市": None,
            '地块公告号': None,
            '区县': None,
            "宗地名称": None,
            "宗地位置": None,
            "地块面积（平方米）": None,
            "用途": None,
            "交易方式": None,
            "出让年限": None,
            "成交价格（万元）": None,
            "受让单位": None,
            "容积率": None,
            "成交时间": None,
            "url": None,
            '成交状态': None,
            '溢价率': None,
        }

    def reqData(self, url, mode=1):
        flag = 5
        while flag:
            try:
                res = self.session.get(url)
                if res.ok:
                    # res.encoding = 'gbk'
                    print('程序抓取成功')
                    if mode == 2:
                        return res.content
                    return res.text
                res -= 1
                print('抓取失败，正在重试')
            except Exception as e:
                res -= 1
                print('抓取发生错误\n%s' % e)

    def parseDecrypt(self, string):
        # 解密文字加密
        font = TTFont('font.woff')
        bestcmap = font['cmap'].getBestCmap()  # 获取cmap节点和name值映射
        cmap = {chr(key): value.replace('*#', '')
                for key, value in bestcmap.items()}
        s = ''
        for ss in string:
            if ss not in ".㎡":
                if cmap[ss] == '*':
                    s += '0'
                else:
                    s += cmap[ss]
            else:
                s += ss
        return s

    def parseHtm(self, htm, result):
        # 解析数据
        soup = BeautifulSoup(htm, 'lxml')
        result['宗地名称'] = soup.find(class_='title').text
        result['宗地位置'] = soup.find(class_='addr-item').text[4:].strip()
        result['地块公告号'] = soup.find(class_='code-text').text
        result['出让年限'] = soup.select_one(
            'body > div.cantainer > div.list-content > div.list-content-left > div:nth-child(1) > ul > li:nth-child(2) > p.main > t').text
        result['交易方式'] = soup.select_one(
            'body > div.cantainer > div.list-content > div.list-content-left > div:nth-child(1) > ul > li:nth-child(1) > p.main > t').text
        s = soup.find(class_='exchange-show exchange-active xn-cf').text
        result['地块面积（平方米）'] = self.parseDecrypt(s)

        details = soup.findAll(class_='base-item')
        result['用途'] = details[5].select_one(
            'div:nth-child(2) > span:nth-child(2)').text.strip()
        result['区县'] = details[0].select_one(
            'div:nth-child(1) > span:nth-child(2)').text.strip()
        result['成交状态'] = details[5].select_one(
            'div:nth-child(1) > span:nth-child(2)').text.strip()
        result['成交时间'] = details[8].select_one(
            'div:nth-child(1) > span:nth-child(2)').text.strip()
        s = details[7].select_one(
            'div:nth-child(2) > span:nth-child(2)').t.text.strip()
        result['起始价格（万元）'] = self.parseDecrypt(s)
        s = details[8].select_one(
            'div:nth-child(2) > span:nth-child(2)').text.strip()
        result['受让单位'] = details[12].select_one(
            'div:nth-child(2) > span:nth-child(2)').text.strip()
        result['容积率'] = details[2].select_one(
            'div:nth-child(1) > span:nth-child(2)').text.strip()
        return result

    def postData(self, id):
        headers = {
            'Cookie': 'acw_tc=76b20f6915846910245541850e72488db705d097c4bf3ea95867bc3e968855; recruitsearchword=%5B%22%5Cu89c4%5Cu5212%5Cu4fdd%5Cu822a%5Cu5317%5Cu4e00%5Cu8def%5Cu4ee5%5Cu5357%5Cu3001%5Cu4e34%5Cu5b89%5Cu8def%5Cu4ee5%5Cu4e1c%22%2C%22%5Cu89c4%5Cu5212%5Cu5de5%5Cu4e1a%5Cu4e1c%5Cu4e00%5Cu8def%5Cu4ee5%5Cu5357%5Cuff0c%5Cu5b59%5Cu6b66%5Cu8def%5Cu4ee5%5Cu4e1c%22%5D; yuanqusearchword=%5B%22%5Cu89c4%5Cu5212%5Cu5de5%5Cu4e1a%5Cu4e00%5Cu8def%22%5D; _dx_uzZo5y=09a433655f8e434b30dbc7d4516f99d14550a3bc9cb3e630c0b0015c69c5e5fad955c70c; _dx_app_8aa57c5b4f2e9459dbe22b2a59178625=5e7af544GnbkUPaDanCkAMrecApr1TMzMQ60J2h1; _dx_captcha_vid=A8EF0B577AE16352B5590BEEE36C865A41440D4F7B9452CA59E2146613DD169AC16A787055F662303D9A6FD9C8989FDF9C1FFA7D5F2D9CF9D7223588C945B3035D10BE8079CC65AF09D244DDF2D65C74; binding-pop=8; PHPSESSID=uu9s32avncg6quakk9emv2sfg6; index_search_status=1; Hm_lvt_3772964c9f7e8f3c48741a29c19196d0=1585061524,1585115682,1585147798,1585157920; referer=https%3A%2F%2Fwww.xuannaer.com%2F; token=0e16bb3f9e5560d090c7027d89eee22dcfcd208495d565ef66e7dff9f98764da; tudiFontName=f866ff8d745f3e2b; sd=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22170f6f21dcb27d-0ef62a7d9e7381-f313f6d-1049088-170f6f21dcc72d%22%2C%22%24device_id%22%3A%22170f6f21dcb27d-0ef62a7d9e7381-f313f6d-1049088-170f6f21dcc72d%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Fwww.xuannaer.com%2Fhenan-zz%2Fzhaopaigua%2Flt1lcd20180101%22%7D%7D; cd=0; Hm_lpvt_3772964c9f7e8f3c48741a29c19196d0=1585158626',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        data = {'id': id, }
        r = self.session.post(
            'https://www.xuannaer.com/Plugin/recruitPrice', data=data, headers=headers)
        return r.json()

    def getMsg(self, li):
        resLi = []
        count = 0
        for url in li:
            if count > 2:
                break
            count += 1
            result = copy.deepcopy(self.resultData)
            htm = self.reqData(url)
            fontUrl = re.findall(
                "'(https://img2.xuannaer.com/static/new/fonts/.*)'\) format\('woff'\),", htm)[0]
            with open('font.woff', 'wb') as f:
                f.write(resUrl(fontUrl, 2))
            id = re.findall(
                'https://www.xuannaer.com/zhaopaigua/detail/(.*)', url)[0]
            data = self.parseHtm(htm, result)
            data['url'] = url
            # restData = self.postData(id)
            # data['成交价格'] = restData['data'][0]
            # data['溢价率'] = restData['data'][3]
            resLi.append(data)
        return resLi


if __name__ == "__main__":
    session = resSession()
    li = []
    for page in range(1, 2):
        url = 'https://www.xuannaer.com/henan-zz/zhaopaigua/lt1lcd20180101/page%s'%page
        htm = resUrl(url)
        dataLi = parseHtml(htm)
        print(dataLi)
        data = session.getMsg(dataLi)
        li += data
    print(li)
