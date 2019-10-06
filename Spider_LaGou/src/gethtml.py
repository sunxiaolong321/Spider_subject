import requests
from urllib import parse

# 构造url post请求


def url_post(url, page=1, headers=None, params=None, keyword=None):
    print("正在爬取第%s页" % page)
    # 构造开始链接，如果没有开始链接会返回请求频繁，链接为首页链接
    url_start = url + "list_%s" % keyword + parse.urlencode(params)
    # 编码问题，也不知道咋回事，需要latin-1编码，只能这么干了
    headers["Referer"] = url_start.encode("utf8").decode("latin-1")

    form_data = {
        'first': 'true',
        'pn': page,
        'kd': keyword
    }

    # 构造请求链接
    url_post = url + "positionAjax.json?"+parse.urlencode(params)
    s = requests.Session()  # 创建一个session对象
    try:
        s.get(url_start, headers=headers, timeout=3)  # 使用session维持同一个会话
        cookie = s.cookies  # 使用该会话的cookie
        response = s.post(url_post, data=form_data,
                          headers=headers, cookies=cookie, timeout=3)
    except:
        print("连接错误，重试中")
        s.get(url_start, headers=headers, timeout=3)  # 使用session维持同一个会话
        cookie = s.cookies  # 使用该会话的cookie
        response = s.post(url_post, data=form_data,
                          headers=headers, cookies=cookie, timeout=3)
    finally:
        return response.json()
