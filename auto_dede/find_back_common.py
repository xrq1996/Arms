# -*- coding: utf-8 -*-
# 四、查找后台地址
#     status：
#         6：已找到
#         7：未找到 -----单独程序跑后台，找到改为6，失败改为8

import traceback
from common import utils
import threading
import requests
from threading import Thread
import time
import tldextract
from unit import dbsqlite

base_back_dict = utils.get_lines("./dict/织梦后台字典.txt")
min_group = 0
thread_num = 1
R = threading.Lock()


def get_domains(status, num=1):
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


def multi_try_common(domains):
    ress = []
    custom_base_bg = ["%s", "admin_%s", "dede_%s", "ad_%s", "bk_%s",
                         "background_%s", "houtai_%s", "%s_admin", "%s_dede",
                         "%s_ad", "%s_bk", "%s_background", "%s_houtai"]
    ns = len(custom_base_bg)
    custom_base_bg.extend(base_back_dict)
    for n in range(len(custom_base_bg)):
        back_dir = custom_base_bg[n]
        for data in domains[:]:
            try:
                domain = utils.format_domain(data[1],protocol=True)
                if n < ns:
                    domain_middle = tldextract.extract(domain).domain
                    bg = back_dir % domain_middle
                else:
                    bg = back_dir
                print(domain + "/" + bg + "/login.php")
                res = utils.my_requests(url=domain + "/" + bg + "/login.php", try_count=1,show_log=False)
                if not res or res.status_code != 200 or "login.php" not in res.url:
                    continue
                res = {"domain": data[1], "res": True, "info": bg}
                ress.append(res)
                domains.remove(data)
            except ConnectionError as e:
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(e)
            except TimeoutError as e:
                print(e)
            except Exception as e:
                traceback.print_exc()
    return ress


def task(i):
    while True:
        try:
            domains = get_domains(status=7,num=10)
            if not domains:
                print('线程：%d,未查到符合条件数据,等待60s...' % i)
                time.sleep(10)
                continue
            ress = multi_try_common(domains)
            d_str = []
            #查找失败的状态：71 -> 8
            for domain in domains:
                for res in ress:
                    if domain[1] == res["domain"]:
                        break
                else:
                    d_str.append(domain[1])
            dbsqlite.batch_data_update(d_str," status = 8")
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