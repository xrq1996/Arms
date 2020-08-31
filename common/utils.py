import requests
import traceback
import base64
import json
from common import variable_storage
import time
from io import BytesIO
from sys import version_info
import random

def get_lines(file_name="target_url", ):
    try:
        with open(file=file_name, encoding="utf-8") as fp:
            domain = "".join(fp.readlines()).split("\n")
            domain = set(domain)
            return domain
    except Exception as e:
        traceback.print_exc()


def my_requests(url, method='get', timeout=15, try_count=3, show_log=False, requester=requests, **args):
    my_headers = variable_storage.headers
    if "headers" in args.keys():
        my_headers = args["headers"]
        args.pop("headers")
    for n in range(try_count):
        try:
            if show_log:
                print("请求：" + url)
            if (variable_storage.change_ip):
                response = requester.request(method=method, url=url, headers=my_headers,
                                             proxies=variable_storage.proxy, timeout=timeout, verify=False, **args)
            else:
                response = requester.request(method=method, url=url, headers=my_headers, timeout=timeout,
                                            verify=False, **args)
            response.encoding = response.apparent_encoding
            if response.status_code == 200:
                return response
        except Exception as e:
            if show_log:
                print(traceback.format_exc())
            if (variable_storage.change_ip):
                variable_storage.proxy = get_proxy()
                print("切换IP:", variable_storage.proxy)
                continue
        if show_log:
            print("请求url:%s失败，剩余重试次数：%d" % (url, n))


def get_proxy():
    variable_storage.proxy_api = "http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=10&time=2&pro=&city=&port=1&format=txt&ss=3&css=&dt=1&specialTxt=3&specialJson=&usertype=2"
    while True:
        res = ""
        try:
            if not variable_storage.proxys:
                res = requests.get(variable_storage.proxy_api, timeout=20).text.strip()
                if res:
                    variable_storage.proxys.extend(res.split("\n"))
            proxy = variable_storage.proxys.pop(0)
            if proxy:
                print("获取代理ip：%s" % proxy)
                return {"http": proxy, "https": proxy}
        except Exception as e:
            # if res
            traceback.print_exc()
            time.sleep(10)


def find_substring(string, substring, times):
    current = 0
    for i in range(1, times + 1):
        current = string.find(substring, current) + 1
        if current == 0: return -1
    print(current-1)
    return current - 1


def group_by_list(data,num):
    data = [data[i:i + num] for i in range(0, len(data), num)]
    return data

def format_domain(url, protocol=False):
    if protocol:
        if "http" not in url:
            url = "http://" + url
        last = find_substring(url, "/", 3)
        last = last if last != -1 else None
        domain = url[:last]
    else:
        domain = url[:find_substring(url, "/", 1)]
    return domain

# 验证码识别
def base64_api(uname, pwd, img):
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(my_requests(method="post",url="http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""




UA = [
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
'Mozilla/5.0+(compatible;+Googlebot/2.1;++http://www.google.com/bot.html)',
]
UA2 = [
'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)',
'Mozilla/5.0+(compatible;+Googlebot/2.1;++http://www.google.com/bot.html)'
]

def get_headers():
    return {"User-Agent": random.choice(UA2)}


if __name__ == '__main__':
    print(format_domain("dede.local.com", True))
