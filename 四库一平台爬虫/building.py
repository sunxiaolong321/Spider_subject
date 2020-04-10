from selenium import webdriver
from requests import Session, cookies
from decrypt import AESDecrypt
import time
import random
import json
import pandas as pd
# 获取详细信息


class detailInfo:
    def __init__(self):
        self.session = Session()
        self.login()

    def random_sleep(self):
        time.sleep(random.randint(5, 10))

    def login(self):
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get(
            'http://jzsc.mohurd.gov.cn/data/project/')
        time.sleep(20)
        c = cookies.RequestsCookieJar()
        for cookie in browser.get_cookies():
            c.set(cookie['name'], cookie['value'])
        headers = {'accessToken': browser.execute_script(
            'return localStorage.getItem("accessToken");'),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        }
        self.session.headers.update(headers)
        self.session.cookies.update(c)
        browser.quit()
        print('建立链接成功')

    def info_map(self, id):
        params = {
            'id': id,
        }
        url = 'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/project/projectDetail'
        r = self.session.get(url, params=params, timeout=5)
        self.random_sleep()
        data = AESDecrypt.decrypt(r.text)
        return data

    def detail_msg(self, id):
        params = {
            'jsxmCode': id,
            'pg': 0,
            'pgsz': 15,
        }
        url = 'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/project/projectCorpInfo'
        r = self.session.get(url, params=params, timeout=5)
        self.random_sleep
        data = AESDecrypt.decrypt(r.text)
        return data


# if __name__ == "__main__":
#     session = detailInfo()
#     sums = []
#     for result in results['result']:
#         # print('正在获取 %s ' % result['宗地名称'])
#         if len(result) == 0:
#             continue
#         name = result['宗地名称']
#         nameId = result['ID']
#         buildingname = result['建设单位']
#         dic = {}
#         try:
#             data = session.info_map(nameId)
#             data = json.loads(data)
#             if data['success'] == False:
#                 dic['项目名称'] = name
#                 continue
#             dic['项目名称'] = data['data']['PRJNAME']
#             dic['建设单位'] = data['data']['BUILDCORPNAME']
#             dic['建设面积'] = data['data']['PRJSIZE']
#             nid = data['data']['PRJNUM']
#             if nid:
#                 data = session.detail_msg(nid)
#                 data = json.loads(data)
#                 li = []
#                 if data['data'] != None:
#                     for d in data['data']['list']:
#                         li.append(d['CORPROLENUM'])
#                         li.append(d['CORPNAME'])
#                 dic['detail'] = li
#         except Exception as e:
#             print(e)
#             dic['项目名称'] = name
#         dic['建设单位(1)'] = buildingname
#         sums.append(dic)
#     f = open('sums.json', 'w', encoding='gbk')
#     results = json.dump({'result': sums}, f, ensure_ascii=False)

if __name__ == "__main__":
    data = pd.read_excel('2.xlsx')
    start = int(input('start: '))
    end = int(input('end: '))
    session = detailInfo()
    sums = []
    error = []
    for nameId in data['ID'][start:end]:
        dic = {}
        try:
            data = session.info_map(nameId)
            data = json.loads(data)
            if data['success'] == False:
                print('抓取失败', end=', ')
                print(nameId)
                error.append(nameId)
                continue
            dic['项目名称'] = data['data']['PRJNAME']
            dic['建设单位'] = data['data']['BUILDCORPNAME']
            dic['建设面积'] = data['data']['PRJSIZE']
            nid = data['data']['PRJNUM']
            if nid:
                data = session.detail_msg(nid)
                data = json.loads(data)
                li = []
                if data['data'] != None:
                    for d in data['data']['list']:
                        if d['CORPROLENUM'] != '勘察企业':
                            li.append(d['CORPROLENUM'])
                            li.append(d['CORPNAME'])
                dic['detail'] = li
        except Exception as e:
            print(e)
            error.append(nameId)
        sums.append(dic)
    f = open('sums.json', 'a', encoding='gbk')
    results = json.dump({'result': sums}, f, ensure_ascii=False)
    pd.DataFrame(error, columns=['url']).to_csv('error.csv', encoding='gbk')
