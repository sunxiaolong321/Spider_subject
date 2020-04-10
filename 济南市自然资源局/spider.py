import time
import requests
import json
import pandas as pd
import random

# def get_proxy():
#     return requests.get("http://127.0.0.1:5145/get/").json()


# def delete_proxy(proxy):
#     requests.get("http://127.0.0.1:5145/delete/?proxy={}".format(proxy))


def index_request(pageNum, cantonId):
    url = 'http://119.164.252.44:8001/data'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    }
    flag = 10
    if flag:
        try:
            # proxy = get_proxy().get("proxy")
            time.sleep(random.randint(0, 2))
            params = {
                'module': 'portal',
                'service': 'Query',
                'method': 'queryFinishedTarget',
                'pageNum': pageNum,
                'pageSize': 20,
                'cantonId': cantonId,
                'status': None,
                'targetNo': None,
                'ms': int(round(time.time() * 1000)),
            }
            r = requests.post(url, headers=headers, params=params, timeout=5)
            if r.ok:
                return r.json()
            flag -= 1
        except:
            # delete_proxy(proxy)
            print('抓取失败，重试中')
            flag -= 1
    print('抓取失败')
    return {}


def detail_request(Id):
    url = 'http://119.164.252.44:8001/data'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        # 'Cookie': 'JSESSIONID=C2CB203B4850D8C166805041E45D1FD4; web=73878830; UM_distinctid=170fb7a70d118d-050f7e405d564b-f313f6d-100200-170fb7a70d26a4; CNZZDATA1260864973=873724809-1584765911-%7C1584765911',
    }
    flag = 10
    if flag:
        # proxy = get_proxy().get("proxy")
        try:
            time.sleep(random.randint(0, 2))
            params = {
                'module': 'portal',
                'service': 'Query',
                'method': 'queryTarget',
                'targetId': Id,
                'ms': int(round(time.time() * 1000)),
            }
            r = requests.post(url, headers=headers, params=params, timeout=5, )
            if r.ok:
                return r.json()
            flag -= 1
        except:
            print('抓取失败，重试中')
            # delete_proxy(proxy)
            flag -= 1
    print('抓取失败')
    return {}


if __name__ == "__main__":
    # js = detail_request(20181108164229738483)
    # with open('detail.json','w',encoding='utf-8') as f:
    #     json.dump(js, f, ensure_ascii=False)
    ids = []
    """
        济南市 370100 1-8
        章丘区 370181 1-5
        平阴县 370124 1-5
        济阳区 370125 1-8
        商河县 370126 1-6
        济南先行区 370117 1-2
        莱芜区 370118 1-2

    """
    count = 1
    city = '莱芜区'
    cantonId = 370118
    for page in range(1, 2):
        print('正在抓取 %d 页信息' % page)
        tmp = index_request(page, cantonId)
        result_data = tmp['result_data']
        for data in result_data:
            print('正在抓取第 %d 条信息' % count)
            count += 1
            targetid = data['targetid']
            ids.append(targetid)
    li = []
    count = 1
    for id in ids:
        msgs = detail_request(id)
    # with open('20200217195041180731.json', 'r', encoding='utf-8') as f:
    #     msgs = json.load(f)
        print('正在解析第 %d 条信息' % count)
        count += 1
        try:
            if len(msgs['goods']) >= 2:
                for msg in msgs['goods']:
                    result = {
                        "用途": None,
                        "编号": None,
                        "行政区": None,
                        '区县': None,
                        "宗地名称": None,
                        "宗地位置": None,
                        "面积（平方米）": None,
                        "交易方式": None,
                        "出让年限": None,
                        '限高': None,
                        "起始价格（万元）": None,
                        "成交价格（万元）": None,
                        "容积率（上限）": None,
                        "容积率（下限）": None,
                        "成交时间": None,
                        "id": None,
                    }
                    result['区县'] = city
                    result['行政区'] = '济南市'
                    result['用途'] = msg['goods_use']
                    result['宗地位置'] = msg['address']
                    result['宗地名称'] = msg['goods_name']
                    result['编号'] = msg['goods_no']
                    result['面积（平方米）'] = msg['land_area']
                    result['交易方式'] = msgs['target']['trans_type_name']
                    result['出让年限'] = msg['use_years']
                    result['起始价格（万元）'] = msg['goods_begin_price']
                    result['成交价格（万元）'] = round(
                        msg['goods_begin_price']*10000/msgs['target']['begin_price']*msgs['target']['trans_price'])/10000
                    result['容积率（上限）'] = msg['plot1_down']
                    result['容积率（下限）'] = msg['plot1_up']
                    result['成交时间'] = msg['end_trans_time']
                    result['限高'] = msg['build_height']
                    result['受让单位'] = msgs['target']['trans_bidder']
                    result['id'] = id
                    li.append(result)
            else:
                msg = msgs['goods'][0]
                result = {
                    "用途": None,
                    "编号": None,
                    "行政区": None,
                    '区县': None,
                    "宗地名称": None,
                    "宗地位置": None,
                    "面积（平方米）": None,
                    "交易方式": None,
                    "出让年限": None,
                    '限高': None,
                    "起始价格（万元）": None,
                    "成交价格（万元）": None,
                    "容积率（上限）": None,
                    "容积率（下限）": None,
                    "成交时间": None,
                    "id": None,
                }
                result['区县'] = city
                result['行政区'] = '济南市'
                result['用途'] = msg['goods_use']
                result['宗地位置'] = msg['address']
                result['宗地名称'] = msg['goods_name']
                result['编号'] = msg['goods_no']
                result['面积（平方米）'] = msg['land_area']
                result['交易方式'] = msgs['target']['trans_type_name']
                result['出让年限'] = msg['use_years']
                result['起始价格（万元）'] = msg['begin_price']/10000
                result['成交价格（万元）'] = msgs['target']['trans_price']/10000
                result['容积率（上限）'] = msg['plot1_down']
                result['容积率（下限）'] = msg['plot1_up']
                result['成交时间'] = msg['end_trans_time']
                result['限高'] = msg['build_height']
                result['id'] = id
                result['受让单位'] = msgs['target']['trans_bidder']
                li.append(result)
        except:
            with open('error.txt', 'w', encoding='gbk') as f:
                f.write(id+'\n')
            result = {
                "用途": None,
                "编号": None,
                "行政区": None,
                '区县': None,
                "宗地名称": None,
                "宗地位置": None,
                "面积（平方米）": None,
                "交易方式": None,
                "出让年限": None,
                '限高': None,
                "起始价格（万元）": None,
                "成交价格（万元）": None,
                "容积率（上限）": None,
                "容积率（下限）": None,
                "成交时间": None,
                "id": id,
            }
            li.append(result)
    pd.DataFrame(li).to_csv('%s.csv' % city, encoding='gbk')
