# -*- coding: utf-8 -*-
### 爆后台路径补充版：通过yourdomain/data/mysql_error_trace.inc猜测类似后台地址。
import re
import os
import requests
from common import utils

def my_requests(url, method='get', timeout=15, try_count=3, **args):
    for n in range(try_count):
        try:
            response = requests.request(method=method, url=url, headers=utils.get_headers(), timeout=timeout, **args)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response
            else:
                print(url+'---request err:'+ str(response.status_code))
                return None
        except Exception as e:
            continue
        print("请求url:%s失败，剩余重试次数：%d" % (url, n))


def get_manger_url(domain_url):
    try:
        arrary = []
        words = ['member', 'plus', 'm']
        title_words = ['后台','系统','管理','内容','系统']
        admin_words = ['houtai', 'adm', 'dede', 'guanli', 'mange']
        select_url = domain_url + "/data/mysql_error_trace.inc"
        response = my_requests(url=select_url)
        is_find = False
        info = ''
        if response:
            response_txt = response.text
            utl_list = re.findall('(?=Page:).*', response_txt)
            for last_url in utl_list:
                last_url = last_url.replace('\r', '').replace('Page:', '').replace(' ', '')
                last_url = last_url[0:last_url.rfind('?')]
                last_url = last_url[0:last_url.rfind('?')]
                if last_url.count('/') >= 2:
                    s = last_url.split('/')[1]
                    if s not in words and s not in arrary and s != '':
                        arrary.append(s)
                        s_url = domain_url + '/' + s + '/'
                        print('try:' + s_url)
                        response2 = my_requests(url=s_url)
                        if response2:
                            try:
                                response2.encoding = response2.apparent_encoding
                                response2_txt = response2.text
                                title = re.findall('<title>.*</title>', response2_txt)[0]
                                if '页面未找到' in title:
                                    continue
                                if any(each in title for each in title_words):
                                    info += s_url+','
                                    is_find = True
                                else:
                                    if any(each in s_url for each in admin_words):
                                        info += s_url + ','
                                        is_find = True
                            except:
                                continue
            res = {"domain": domain_url, "res": is_find, "info": info.strip(',')}
            if len(arrary) == 0:
                print(domain_url + '未找到相对于目录')
        else:
            res = {"domain": domain_url, "res": is_find, "info": '未找到文件'}
        return res
    except:
        return {"domain": domain_url, "res": False, "info": '程序异常'}

