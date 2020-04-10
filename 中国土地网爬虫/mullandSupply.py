# eoding=gbk
import os
import random
import time
import csv
from multiprocessing import Pool
import execjs
from bs4 import BeautifulSoup
from requests import Session
import pandas as pd


class landSupply():
    def __init__(self):
        self.session = Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        }
        self.keep_live()

# 已经失效，已经复活
    def keep_live(self):

        def js_deal():
            stringToHexJs = """
            function stringToHex(str) {
                val = "";
                for (var i = 0; i < str.length; i++) {
                    if (val == "") val = str.charCodeAt(i).toString(16);
                    else val += str.charCodeAt(i).toString(16);
                }
                return val;
            }
            function YunSuoAutoJump() {
                var width = 768;
                var height = 1366;
                var screendate = width + "," + height;
            //  var curlocation = window.location.href;
            //  if (-1 == curlocation.indexOf("security_verify_")) {
            //        document.cookie = "srcurl=" + stringToHex(window.location.href) + ";path=/;";
            return "&security_verify_data=" + stringToHex(screendate);
            }
            """
            ctx = execjs.compile(stringToHexJs)
            scrurl = ctx.call("YunSuoAutoJump")
            return scrurl

        url = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'
        Flag = 5
        while(Flag):
            try:
                Flag = False
                self.session.get(url, headers=self.headers, timeout=(3, 5))
                time.sleep(2)
                self.session.get(
                    url+js_deal(), headers=self.headers, timeout=(3, 5))
                print('建立链接成功')
            except Exception as e:
                Flag -= 1
                if Flag == 0:
                    print(e)
                    raise e
                print("连接%s失败，正在重试" % url)

# 新的解析方式
    # def keep_live(self):
    #     def js_deal():
    #         stringToHexJs = """
    #          function EnterJump() {
    #             if (event.keyCode == 13) {
    #                 YunsuoAutoJump();
    #             }
    #         }
    #         function stringToHex(str) {
    #             var val = "";
    #             for (var i = 0; i < str.length; i++) {
    #                 if (val == "")
    #                     val = str.charCodeAt(i).toString(16);
    #                 else
    #                     val += str.charCodeAt(i).toString(16);
    #             }
    #             return val;
    #         }
    #         function YunsuoAutoJump() {
    #             var width = 768;
    #             var height = 1366;
    #             var screendate = width + "," + height;
    #             var text = document.getElementById("intext").value;
    #             if (text == "") {
    #                 alert('验证码不能为空');
    #             } else {
    #                 // var curlocation = window.location.href;
    #                 // if (-1 == curlocation.indexOf("security_verify_")) {
    #                 //     document.cookie = "srcurl=" + stringToHex(window.location.href) + ";path=/;";
    #                  }
    #                 self.location = "/default.aspx?tabid=263&security_verify_img=" + stringToHex(text);
    #             }
    #         """
    #     url = 'https://www.landchina.com/default.aspx?tabid=263'
    #     self.session.get(url, )

    def get_url(self, url):
        Flag = 5
        while(Flag):
            try:
                Flag = False
                response = self.session.get(
                    url, headers=self.headers, timeout=(8, 10))
                print('成功抓取链接')
            except Exception as e:
                Flag -= 1
                if Flag == 0:
                    print(e)
                    raise e
                print("连接%s失败，正在重试" % url)
        response.encoding = 'gbk'
        return response.text

    def parse_html(self, html):
        try:
            soup = BeautifulSoup(html, "lxml")
            data = {
                "省市": None,
                '区县': None,
                # "电子监管号": None,
                "宗地名称": None,
                "宗地位置": None,
                "面积（公顷）": None,
                # "土地来源": None,
                "用途": None,
                "交易方式": None,
                # "行业分类": None,
                "出让年限": None,
                # "土地级别": None,
                "成交价格（万元）": None,
                "受让单位": None,
                # "分期支付约定：1期": None,
                # "分期支付约定：2期": None,
                # "分期支付约定：3期": None,
                # "分期支付约定：4期": None,
                "约定容积率（上限）": None,
                "约定容积率（下限）": None,
                # "约定开工时间": None,
                # # "约定交地时间": None,
                # # "约定竣工时间": None,
                "成交时间": None,
                "url": None,
            }
            # 行政区
            data["省市"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2")[0].text.strip()
            # 电子监管号
            # data["电子监管号"] = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl")[0].text
            # 项目名称
            data["宗地名称"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl")[0].text.strip()
            # 项目位置
            data["宗地位置"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl")[0].text.strip()
            # 面积（公顷）
            data["面积（公顷）"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl")[0].text.strip()
            # 土地来源
            # 判断土地来源需要函数来判断
            # number = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl")[0].text
            # if number == data["面积（公顷）"]:
            #     data["土地来源"] = "现有建设用地"
            # elif number == 0.0:
            #     data["土地来源"] = "新增建设用地"
            # else:
            #     data["土地来源"] = "新增建设用地(来自存量库)"
            # 土地用途
            data["用途"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2")[0].text.strip()
            # 供地方式
            data["交易方式"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl")[0].text.strip()
            # data["行业分类"] = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl")[0].text
            data["出让年限"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2")[0].text.strip()
            # data["土地级别"] = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2")[0].text
            data["成交价格（万元）"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl")[0].text.strip()

            data["受让单位"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl")[0].text.strip()
            if data['受让单位'] == '':
                data["受让单位"] = soup.select(
                    "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r23_c2")[0].text.strip()
            # x = soup.select("#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3 > tbody")[
            #     0].text
            # count = 1
            # for term in list(reversed(re.findall(r"\d{4}年\d{2}月\d{2}日\d+.\d{4}", x)[1:])):
            #     data["分期支付约定：%d期" % count] = term
            #     count += 1
            data["约定容积率（上限）"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl")[0].text.strip()
            data["约定容积率（下限）"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl")[0].text.strip()
            # data["约定开工时间"] = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2_ctrl")[0].text
            # data["实际开工时间"] = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c2")[0].text.strip()
            # data["约定交地时间"] = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c2")[0].text
            # data["约定竣工时间"] = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4")[0].text
            # data["实际竣工时间"] = soup.select(
            #     "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c4")[0].text.strip()
            data["成交时间"] = soup.select(
                "#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4")[0].text.strip()
        except Exception as e:
            print(e)
            print("抓取失败")
            return {}
        return data

    def parse_msg(self, url):
        try:
            html = self.get_url(url)
            data = self.parse_html(html)
        except:
            print("抓取链接 %s 失败,存入 error.txt 中" % url)
            with open('error.txt', 'a', encoding='utf-8') as f:
                f.write(url+'\n')
        return data

    def close_session(self):
        print("链接已经关闭")
        self.session.close()


if __name__ == "__main__":
    session = landSupply()
    for file in os.listdir("merge_data"):
    # file = '住宅用地.csv'
    # p = Pool(5)
        if file != '工矿仓储用地.csv':
            continue
        all_result = []
        print('正在抓取%s' % file[:-4])
        with open("./merge_data/"+file, 'r', encoding='utf-8') as f:
            csv_data = csv.reader(f)
            count = 1
            for detail_msg in csv_data:
                if detail_msg[2] != "url" and len(detail_msg[2]) != 0:
                    print('正在抓取第 %d 条信息：%s' % (count, detail_msg[1]))
                    count += 1
                    data = session.parse_msg(detail_msg[2])
                    # data = p.apply_async(
                    #     session.parse_msg, args=(detail_msg[2], )).get()
                    if len(data) != 0:
                        data['url'] = detail_msg[2]
                        data['区县'] = detail_msg[1]
                    all_result.append(data)
            # p.close()
            # p.join()
        try:
            pd.DataFrame(all_result).to_csv('./result/u%s' % file)
        except:
            pass
        try:
            with open("./result/csv%s" % file, 'w', encoding='gbk', newline='') as f:
                csv_writer = csv.writer(f)
                for d in all_result:
                    try:
                        csv_writer.writerow([a for a in d.values()])
                    except:
                        print(d)
        except:
            pass
        pd.DataFrame(all_result).to_csv('./result/%s' %
                                        file, encoding='gbk')
