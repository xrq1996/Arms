# -*- coding: utf-8 -*-
# @Time : 2020/4/24 15:12
# @Author : longe
# @File : baidu_link.py
# @Software: PyCharm

import re
import requests
import xlrd
import time
from lxml import etree
import json
import os
import threading
import urllib.request

def save_domain(file_path,domains):
    with open(file_path, "a") as f:
        for domain in domains:
            f.write(domain + '\n')

class BAIDU_LINK(object):
    def __init__(self):
        self.bd_headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'BIDUPSID=1BF513B9C7A2845F0A1F149AE3660056; PSTM=1584106019; BAIDUID=1BF513B9C7A2845F4E9BCE5A269460CC:FG=1; BD_UPN=12314753; BDUSS=ZWV21TbHJUNE1jdTktWGxuemp0MWItWWVvclJpSFZpMDRlV0JQYU5JbldUc0plRVFBQUFBJCQAAAAAAQAAAAEAAABeR~QUYWRtaW42Njc3ODgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANbBml7WwZpeZG; BDSFRCVID=bGCOJeC62G7CMwouCfSOesrkQLt0ZgbTH6aIDaP0oQKdTISxi1USEG0PDx8g0Ku-bRAYogKKLmOTHPFF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRk8_KtKtCI3HnRY-P4_-tAt2qoXetJyaR3P2DJvWJ5TMCojbPcP-UI0LPCHhPQe-D3I_x0yXbQjShPC-tn2hRtQBPO8tnLHfT5fBt5D3l02VM7Ee-t2ynLV34uHe4RMW23rWl7mWUJPsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjjCae5Q-Da_Dq6n2aIOt0Tr25RrjeJrmq4bohjP9KMR9BtQmJJrO-fn9MtQhEpcpqto5K4PuD4PftUJZQg-q3R7GQl6zVq7-Dqb-Qn893UTn0x-jLITOVn0MW-5DDI3cD-nJyUPThtnnBpOl3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CFhfIKBhKKlejRjh-40b2TJK4625CoJsJOOaCvUMCbOy4oTj6j3jx5uLh3t02QK0n5b-JvGHJOvBpn-3MvB-fn7-UktJNn7atOvtD5_DCbeQft20-LEeMtjBbQaabvWon7jWhvdDq72yh3PQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCOJTk8tbPJVb3qKRTsDTrnh6RDQUtgyxomtjjxJ27uLb7a0bQ68n5RK4RGXb3QWxJaLUkqKm5R3xtMaMjveMbV0n7EDqL9QttjQU3OfIkja-KEKfoNoJ7TyURdhf47yb3l0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRQ2QJ8BtD0BMDQP; H_PS_PSSID=31356_1426_31124_21109_31342_30909_31229_30823_31086_31163; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=7; H_PS_645EC=b68cofwr9QOT6kspYlI93Nft5vBFk0MRNihyLltAivUA%2BvD%2BcJprirn%2B8YM',
            'Host': 'www.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.common_headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def get_page_from_url(self, url, headers=None):
        """
        提取url
        :param url:
        :return:
        """
        page = requests.get(url, headers=headers, timeout=10)
        # print(html)
        return page

    def read_url(self,dirname):
        with open(file="kw.txt",encoding="utf-8") as f:
            fall = f.read().split("\n")
            for l in range(0,len(fall)):
                kw=fall[l]
                if kw.split("----")[0] == 'bd':
                    self.get_bd_url(kw.split("----")[1],dirname)
                if kw.split("----")[0] == 'gg':
                    self.get_gg_url(kw.split("----")[1],dirname)


    def get_bd_url(self,kw,dirname):
        print(kw)
        filename=kw.replace(" ","_").replace(":","_").replace("?","_").replace(",","_").replace(".","_")[:10]
        if_continue = True
        for p in range(0,500, 50):
            links = []
            if not if_continue:
                print("百度搜索结果采集结束")
                break
            keyword = urllib.parse.urlencode({'wd': kw})
            url='http://www.baidu.com/s?'+keyword+'&rn=50&pn=' + str(p)
            print("百度搜索结果采集中...%s"%url)
            try:
                res=self.get_page_from_url(url=url,headers=self.bd_headers)
                time.sleep(1)
            except Exception:
                print('site请求失败!',url)
            res.encoding="utf-8"
            html=res.text
            if "下一页" not in html:
                if_continue = False
            tree=etree.HTML(html)
            ree=tree.xpath('//div[@id="content_left"]/div[position()>1]/h3/a/@href')
            if len(ree)==0:
                pass
            else:
                for link_url in ree:
                    try:
                        r= requests.get(link_url, allow_redirects=False,timeout=10)
                        if int(r.status_code)==302:
                            domain = r.next.url
                            domain = re.findall("[http://,https://]+.+?/+", domain)[0][:-1]
                            print(domain)
                            if domain not in all_links:
                                all_links.add(domain)
                                links.append(domain)
                    except Exception as ex:
                        print(ex)
            save_domain(dirname+"/"+filename+'.txt',links)


    def get_gg_url(self,kw,dirname):
        gg_key = "AIzaSyCKgCWIiSINI6SyxtgXDaEYkTn7CyCFu9k"
        cx = "013924116114311910003:_n8udj-eyx8"
        search_url="https://www.googleapis.com/customsearch/v1?key=%s&q=%s&cx=%s&start={}&num=10&lr=lang_zh-CN" % (gg_key,kw,cx)
        print(kw)
        filename=kw.replace(" ","_").replace(":","_").replace("?","_").replace(",","_").replace(".","_")[:10]
        if_continue = True
        i = 1
        while i<100:
            url = search_url.format(i)
            print(i)
            page = self.get_page_from_url(url=url,headers=self.common_headers)
            data_list = []
            links = []
            if json.loads(page.content.decode())["items"]:
                data_list = json.loads(page.content.decode())["items"]
                for data in data_list:
                    domain = re.findall("[http://,https://]+.+?/+", data["link"])[0][:-1]
                    if domain not in all_links:
                        all_links.add(domain)
                        links.append(domain)
            else:
                print("no item")
            save_domain(dirname+"/"+filename+'.txt',links)
            if json.loads(page.content.decode())["queries"]["nextPage"]:
                i += 10
            else:
                break
                        



if __name__ == '__main__':
    # filter_url = False
    dirname='搜索结果'
    all_links = set()
    baidu_link=BAIDU_LINK()
    baidu_link.read_url(dirname)