from selenium import webdriver
import csv
import time

title = '公共管理与公共服务用地'

# 浏览器信息
options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
    'Safari/537.36"')
browser = webdriver.Chrome(options=options)


url = "https://www.landchina.com/default.aspx?tabid=263&ComName=default"
browser.get(url)
browser.implicitly_wait(5)

browser.find_element_by_css_selector("#TAB_QueryConditionItem270").click()
browser.find_element_by_css_selector(
    "#TAB_queryDateItem_270_1").send_keys("2018-1-1")
browser.find_element_by_css_selector(
    "#TAB_queryDateItem_270_2").send_keys("2020-3-31")
# 处理枚举选择器
flag = True
count = 0
while(flag):
    if count >= 5:
        print("获取行政区失败")
        break
    try:
        flag = False
        browser.find_element_by_css_selector(
            "#TAB_queryTblEnumItem_256").click()
        time.sleep(2)
        all_handles = browser.window_handles
        browser.switch_to.window(all_handles[1])
        # browser.find_element_by_css_selector("#treeDemo_15_switch").click()
        browser.find_element_by_xpath("//*[@title='广东省']/../span[1]").click()
        time.sleep(2)
        # while(browser.find_element_by_css_selector("#treeDemo_35_span").text == "undefined"):
        #     # browser.find_element_by_css_selector("#treeDemo_15_switch").click()
        #     browser.find_element_by_xpath(
        #         "//span[contains(text(),'广东省')]").click
        #     time.sleep(2)
        # browser.find_element_by_css_selector("#treeDemo_35_a").click()
        browser.find_element_by_xpath("//*[@title='广州市']").click()
        time.sleep(2)
        browser.find_element_by_css_selector(
            "#Table1 > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(3) > input:nth-child(1)").click()
    except:
        flag = True
        browser.close()
        browser.switch_to.window(all_handles[0])
        count += 1

browser.switch_to.window(all_handles[0])
flag = True
count = 0
while(flag):
    if count >= 5:
        print("住宅用地")
        break
    try:
        flag = False
        browser.find_element_by_css_selector(
            "#TAB_queryTblEnumItem_212").click()
        time.sleep(2)
        all_handles = browser.window_handles
        browser.switch_to.window(all_handles[1])
        browser.find_element_by_css_selector("#treeDemo_2_switch").click()
        time.sleep(2)
        # browser.find_element_by_css_selector("#treeDemo_4_ico").click()
        browser.find_element_by_xpath("//*[@title='%s']"%title).click()
        time.sleep(2)
        browser.find_element_by_css_selector(
            "#Table1 > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(3) > input:nth-child(1)").click()
    except:
        flag = True
        browser.close()
        browser.switch_to.window(all_handles[0])
        count += 1


# 查询
browser.switch_to.window(all_handles[0])
browser.find_element_by_css_selector("#TAB_QueryButtonControl").click()

flag = True
page = 1
while(flag):
    f = open("./result/%s%d.csv" %
             (title, page), 'w', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    for message in browser.find_elements_by_class_name("gridItem"):
        csv_writer.writerow([message.find_element_by_css_selector(
            "td:nth-child(2)").text, message.find_element_by_css_selector(
            "td:nth-child(3) > a").get_attribute('href')])
    for message in browser.find_elements_by_class_name("gridAlternatingItem"):
        csv_writer.writerow([message.find_element_by_css_selector(
            "td:nth-child(2)").text, message.find_element_by_css_selector(
            "td:nth-child(3) > a").get_attribute('href')])
    f.close()
    try:
        print("已经保存完第 %d 页" % page)
        time.sleep(2)
        page += 1
        browser.find_element_by_xpath("//*[text()='下页']").click()
        time.sleep(2)
    except:
        print("第%d页发生错误" % page)
        flag = False
