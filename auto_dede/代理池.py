# -*- coding: utf-8 -*-

import re
import os
import requests
from common import utils
import json
import datetime
import time
from threading import Thread
proxy_list = []
log_list = []

# 接口请求IP
def request_ip(method='get', timeout=15, try_count=3, **args):
    try:
        url = "http://d.jghttp.golangapi.com/getip?num=5&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions="
        response = requests.request(method=method, url=url, headers=utils.get_headers(), timeout=timeout, **args)
        s = []
        if response.status_code == 200:
            data = json.loads(response.text)
            if data['code'] == 0:
                s = data['data']
        return s
    except Exception as e:
        return []


# 时间对比方法
def compare_time(time1, time2, second=50):
    d1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
    delta = d1 - d2
    if delta.seconds >= second:
        return True
    else:
        return False


# 检查过期IP,独立线程运行
def check_proxy(sleep=5, proxy_max_count=4):
    while True:
        try:
            for proxy in proxy_list:
                time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if not compare_time(proxy['expire_time'], time1):
                    proxy_list.remove(proxy)
                    print('移除:%s' % proxy)
            if len(proxy_list) < proxy_max_count:
                proxy_list.extend(request_ip())
                print('数量不够，请求新IP，现池中IP数:%d' % len(proxy_list))
        except Exception as e:
            print(e)
        print('下次检查过期IP：%d秒后' % sleep)
        time.sleep(sleep)


def get_ip(domain=None):
    try:
        if domain:
            for proxy in proxy_list:
                if 'use_domain' in proxy:
                    if domain in proxy['use_domain']:
                        continue
                    proxy_list.remove(proxy)
                    proxy['use_domain'] += ','+domain
                    proxy_list.append(proxy)
                else:
                    proxy_list.remove(proxy)
                    proxy['use_domain'] = domain
                    proxy_list.append(proxy)
                return proxy
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    # try:
    #     Threads = []
    #     for i in range(1):
    #         t = Thread(target=check_proxy)
    #         Threads.append(t)
    #         t.start()
    #     # 启动所有线程
    #     for i in Threads:
    #         i.join()
    # except Exception as e:
    #     print(e)
    Thread(target=check_proxy).start()
    for i in range(8):
        get_ip(domain='www.baidu.com')
