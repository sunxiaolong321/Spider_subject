import json
import time
import random
import pandas as pd
import requests
from faker import Factory

from decrypt import AESDecrypt


def index_msg(buildCorpName):
    params = {
        # 'prjectName': projectName,
        'buildCorpName': buildCorpName,
        'pg': 0,
        'pgsz': 15,
        'total': 0
    }
    flag = 5
    ua = Factory.create()
    headers = {
        'User-Agent': ua.user_agent()
    }
    while flag:
        url = 'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/project/list'
        r = requests.get(url, params=params, headers=headers, timeout=5)
        time.sleep(random.randint(1, 5))
        if not r.ok:
            flag -= 1
            continue
        return AESDecrypt.decrypt(r.text)


if __name__ == '__main__':
    data = pd.read_excel('福州-公建数据.xlsx')
    li = []
    for da in data['受让单位'].drop_duplicates():
        # print(da)
        print('正在抓取 %s' % da)
        flag = 5
        while flag:
            js = json.loads(index_msg(da))
            if js['success'] == False:
                flag -= 1
                if flag <= 0:
                    f = open('error.txt', 'w', encoding='gbk')
                    f.write(da+'\n')
            else:
                for d in js['data']['list']:
                    dic = {}
                    dic['项目名称'] = d['BUILDCORPNAME']
                    dic['ID'] = d['ID']
                    dic['建设单位'] = d['BUILDCORPNAME']
                    print(d)
                    li.append(dic)
                flag = 0
    pd.DataFrame(li).to_excel('2.xlsx')
