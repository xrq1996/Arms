# -*- coding: utf-8 -*-
#深度爬取友链
# 表：doamintable
# domain 网址，is_crawl 是否已经采集友链， status：0-刚入库、1-打不开、

import re
import os
import threading
import urllib
from unit import dbsqlite
import time
import requests
from common import utils
import tldextract



def my_requests(url, method='get', timeout=15, try_count=3, **args):
    for n in range(try_count):
        try:
            response = requests.request(method=method, url=url, headers=utils.get_headers(), timeout=timeout, **args)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response
            else:
                print(url+' ,   request err:'+ str(response.status_code)+ ',重试次数%d' % n)
                continue
        except Exception as e:
            print(e)
            continue
        print("请求url:%s失败，剩余重试次数：%d" % (url, n))

def getUrllist(htmlcode,ys_url):
    reg = r' href="(.+?)"'
    urllist = list()
    urllist.append(ys_url)
    reg_href = re.compile(reg)
    href_list = reg_href.findall(htmlcode)
    for href in href_list:
        url = str(href)
        url.strip()
        if not url.startswith("#") and not url.endswith('#'):
            if not url.startswith('<') and not url.endswith('>'):
                if not url.endswith('.xml') and not url.endswith('.ico') and not url.endswith('.js') and not url.endswith('css'):
                    if '.' in url:
                        o = tldextract.extract(url)
                        if o.domain !='' and o.suffix !='':
                            o_ys = tldextract.extract(ys_url)
                            if o.domain != o_ys.domain and o.suffix != o_ys.suffix and 'gov' not in o.suffix:
                                s =urllib.parse.urlparse(url)
                                scheme = s.scheme
                                if scheme =="":
                                    scheme = 'http'
                                url = scheme+"://"+ s.netloc
                                if url not in urllist:
                                    urllist.append(url)
    return urllist

def crawling(i):
    while True:
        try:
            domain_model = dbsqlite.data_getlist(' is_crawl = 0 ')
            if not domain_model:
                print('线程：%d为查到采集源,等待3s'% i)
                time.sleep(3)
                continue
            url = domain_model[1]
            print('线程%d:%s'% (i,url))
            response = my_requests(url)
            if response:
                urllist = getUrllist(response.text,url)
                for curl in urllist:
                    #s = urllib.parse.urlparse(url).netloc
                    if dbsqlite.data_select(curl):
                        continue
                    dbsqlite.data_insert(curl)
            else:
                dbsqlite.data_update(url,'status = 1')
        except Exception as e:
            print(e)
            continue

def load_url_txt():
    path = './res/注册成功'
    list = utils.get_lines(path)
    for url in list:
        if dbsqlite.data_select(url):
            continue
        dbsqlite.data_insert(url)
    print('导入初始数据：%d条' % len(list))

if __name__ == '__main__':
    load_url_txt()
    try:
        Threads = []
        for i in range(10):
            t = threading.Thread(target=crawling, args=(i,))
            t.daemon = 1
            Threads.append(t)
            t.start()
        # 启动所有线程
        for i in Threads:
            i.join()
    except Exception as e:
        print(e)

