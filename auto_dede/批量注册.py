# -*- coding: utf-8 -*-
from common import utils
import requests
from PIL import Image
import traceback
from common import variable_storage
import re
from common import utils
# re.findall('(?<=document.write\()\S+(?="\);)',res.text)

def post_data(session, domain, vcode, uname="0000001"):
    try:
        params = {"dopost": "regbase", "step": 1, "mtype": "个人", "mtype": "个人", "userid": uname, "uname": "0000001",
                  "userpwd": "qwe123", "userpwdok": "qwe123", "email": "ldanche@protonmail.com", "safequestion": 0,
                  "safeanswer": "", "sex": "", "agree": ""}
        params.update({"vdcode": vcode})
        res = utils.my_requests(url=domain + "/member/reg_new.php", params=params,timeout=10,requester=session)
        return res
    except Exception as e:
        traceback.print_exc()
        return False


def 注册(domain, num=5):
    try:
        session = requests.session()
        res = session.get(domain + variable_storage.dede_vc_url,timeout=10)
        if res.status_code != 200:
            res = session.get(domain + "/library/vdimgck.php", timeout=10)
        with open(file="./tp.jpg", mode="wb") as fp:
            fp.write(res.content)
        img_path = "./tp.jpg"
        img = Image.open(img_path)
        result = utils.base64_api(uname=variable_storage.vcode_pm_uname, pwd=variable_storage.vcode_pm_pwd, img=img)
        res = post_data(session, domain, result)
        if not res:
            raise Exception
        if "成功" in res.text or "模型不存在" in res.text or "完成基本信息的注册" in res.text:
            return {"domain":domain,"res":True,"info":"注册成功"}
        elif "已存在" in res.text or "重复" in res.text or "用户名" in res.text:
            res = post_data(session, domain, result, uname=variable_storage.mail)
            if "成功" in res.text or "模型不存在" in res.text or "完成基本信息的注册" in res.text:
                return {"domain":domain,"res":True,"info":"注册成功"}
            else:
                message = re.findall('(?<=document.write\()\S+(?="\);)',res.text)[0]
                return {"domain":domain,"res":False,"info":message}
        else:
            return {"domain":domain,"res":False,"info":"连接失败"}
    except Exception as e:
        if num > 0:
            print("尝试重新注册：" + domain)
            return 注册(domain, num - 1)
        else:
            traceback.print_exc()
            return {"domain":domain,"res":False,"info":"未知异常"}

def main():
    while True:
        # get domain
        domain = "http://www.c-dz.com/"
        res = 注册(domain=domain)
        #结果入库



if __name__ == "__main__":
    #单线程运行
    main()