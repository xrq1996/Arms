import traceback
import time
from threading import Thread
from 织梦 import utils
import random


def get_domains(file_name="target_url",):
    try:
        with open(file=file_name,encoding="utf-8") as fp:
            domain = "".join(fp.readlines()).split("\n")
            return domain
    except Exception as e:
        traceback.print_exc()

def scan_member_register():
    while domains:
        domain = domains.pop()
        print("处理：%d"%(n - len(domains)))
        t = time.time()
        if "http" not in domain:
            domain = "http://" + domain
        try:
            res = utils.my_requests(url=domain + "/member/index_do.php?dopost=checkuser&fmdo=user&cktype=1&uid=0000001", timeout=5, try_count=2)
            if res.status_code == 200 and "用户名可以使用" in res.text:
                ress.append(domain)
                print("%s:%s" % (domain, "用户名可以使用"))
            else:
                pass
                # print("%s:扫描失败" % domain)
        except Exception as e:
            # print(e)
            pass
            # print("%s:扫描失败"%domain)
        print(time.time() - t)

def scan():
    while domains:
        domain = domains.pop()
        print(len(domains))
        if "http" not in domain:
            domain = "http://" + domain
        try:
            res = requests.get(url=domain + "/data/admin/ver.txt", timeout=10)
            if res.status_code == 200 and len(res.text) < 20:
                ress.append(domain)
                print("%s:%s" % (domain, res.text))
            else:
                continue
                print("%s:扫描失败" % domain)
        except:
            continue
            print("%s:扫描失败"%domain)

def task(t_num):
    for n in range(t_num):
        print("线程%d启动" % n)
        time.sleep(0.5)
        t = Thread(target=scan_member_register)
        t.start()
        ts.append(t)
    for t in ts:
        t.join()
    print("结果")
    print(ress)

if __name__ == '__main__':
    # 线程数
    t_num = 200
    ts = []
    domains = utils.get_lines("./验证注册")
    n = len(domains)
    #结果集
    ress = []
    task(t_num)
    with open(file="./res/注册扫描结果",mode="a") as fp:
        fp.write("\n扫描结果|%s\n" % str(time.time()))
        fp.writelines("\n".join(ress))