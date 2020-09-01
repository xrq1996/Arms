# -*- coding: utf-8 -*-
# 深度爬取友链
# 表：doamintable
# domain 网址，is_crawl 是否已经采集友链， status：0-刚入库、1-打不开、

import re
import os
from threading import Thread
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
                # print(url + ' ,   request err:' + str(response.status_code) + ',重试次数%d' % n)
                continue
        except Exception as e:
            print(e)
            continue
        # print("请求url:%s失败，剩余重试次数：%d" % (url, n))


def getUrllist(htmlcode, ys_url):
    reg = r' href="(.+?)"'
    urllist = list()
    reg_href = re.compile(reg)
    href_list = reg_href.findall(htmlcode)
    for href in href_list:
        url = str(href)
        url.strip()
        if not url.startswith("#") and not url.endswith('#'):
            if not url.startswith('<') and not url.endswith('>'):
                if not url.endswith('.xml') and not url.endswith('.ico') and not url.endswith(
                        '.js') and not url.endswith('css'):
                    if '.' in url:
                        if not (utils.format_domain(url, protocol=True).replace("http://","").replace("https://","") == utils.format_domain(ys_url, protocol=True).replace("http://","").replace("https://","")):
                            o = tldextract.extract(url)
                            if o.domain != '' and o.suffix != '':
                                o_ys = tldextract.extract(ys_url)
                                # and o.suffix != o_ys.suffix
                                if o.domain != o_ys.domain and 'gov' not in o.suffix:
                                    s = urllib.parse.urlparse(url)
                                    scheme = s.scheme
                                    if scheme == "":
                                        scheme = 'http'
                                    url = scheme + "://" + s.netloc
                                    if url not in urllist and o.domain not in urllist:
                                        urllist.append(url)
    return urllist


def crawling(i):
    while True:
        try:
            #title_words = ['银行', '政府', '管理', '内容', '系统']
            path = './dict/采集标题过滤字典.txt'
            title_words = utils.get_lines(path)
            domain_model = dbsqlite.data_getlist(' is_crawl = 0 ')
            if not domain_model:
                print('线程：%d未查到采集源,等待3s' % i)
                time.sleep(3)
                continue
            url = domain_model[1]
            print('线程%d:%s' % (i, url))
            response = my_requests(url)
            if response:
                response.encoding = response.apparent_encoding
                response2_txt = response.text
                title = re.findall('<title>(.+)</title>', response2_txt)[0]
                if any(each in title for each in title_words):
                    dbsqlite.data_update(url, "title = '%s',status = 1" % title)
                    continue
                else:
                    dbsqlite.data_update(url, "title = '%s'" % title)
                urllist = getUrllist(response.text, url)
                print('%s友链数:%d' % (url,len(urllist)))
                for curl in urllist:
                    # s = urllib.parse.urlparse(url).netloc
                    try:
                        res = utils.my_requests(url=curl,try_count=1, timeout=10)
                        if res:
                            curl = utils.format_domain(res.url,protocol=True)
                        else:
                            continue
                    except Exception as e:
                        continue
                    if dbsqlite.data_select(curl):
                        continue
                    dbsqlite.data_insert(curl)
            else:
                dbsqlite.data_update(url, 'status = 1')
        except Exception as e:
            print(e)
            continue


def load_url_txt():
    try:
        path = './dict/导入采集种子'
        list = utils.get_lines(path)
        for url in list:
            url = 'http://www.'+ url
            # if dbsqlite.data_select(url):
            #     continue
            dbsqlite.data_insert(url)
        print('导入初始数据：%d条' % len(list))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # crawling(1)
    dbsqlite.data_creat()
    # load_url_txt()
    try:
        Threads = []
        for i in range(100):
            t = Thread(target=crawling, args=(i,))
            t.daemon = 1
            Threads.append(t)
            t.start()
        # 启动所有线程
        for i in Threads:
            i.join()
    except Exception as e:
        print(e)
