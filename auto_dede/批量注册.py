# -*- coding: utf-8 -*-
from common import utils
import requests
from PIL import Image
import traceback
from common import variable_storage
import re
from common import utils
# re.findall('(?<=document.write\()\S+(?="\);)',res.text)

def post_data(session, domain, vcode, uname="0000001",dopost="regbase"):
    try:
        params = {"dopost": dopost, "step": 1, "mtype": "个人", "mtype": "个人", "userid": uname, "uname": "0000001c",
                  "userpwd": "qwe123", "userpwdok": "qwe123", "email": "ldanche@protonmail.com", "safequestion": 0,
                  "safeanswer": "", "sex": "", "agree": ""}
        params.update({"vdcode": vcode})
        res = utils.my_requests(url=domain + "/member/reg_new.php", params=params,timeout=10,requester=session)
        return res
    except Exception as e:
        traceback.print_exc()
        return False


def 注册(domain, num=3):
    try:
        session = requests.session()
        res = session.get(domain + variable_storage.dede_vc_url,timeout=10)
        if res.status_code != 200:
            res = session.get(domain + "/library/vdimgck.php", timeout=10)
        with open(file="./tp.jpg", mode="wb") as fp:
            fp.write(res.content)
        if res.status_code != 200:
            return {"domain":domain,"res":False,"info":"非织梦，状态码：%d" % res.status_code}
        img_path = "./tp.jpg"
        try:
            img = Image.open(img_path)
        except:
            return {"domain": domain, "res": False, "info": "非织梦，状态码：%d" % res.status_code}
        result = utils.base64_api(uname=variable_storage.vcode_pm_uname, pwd=variable_storage.vcode_pm_pwd, img=img)
        res = post_data(session, domain, result)
        if not res:
            raise ConnectionError
        if res.status_code!=200:
            return {"domain":domain,"res":False,"info":"注册状态：%d"%res.status_code}
        if "成功" in res.text or "模型不存在" in res.text or "完成基本信息的注册" in res.text:
            return {"domain":domain,"res":True,"info":"0000001"}
        elif "存在" in res.text or "重复" in res.text :
            res = post_data(session, domain, result, uname=variable_storage.mail)
            if "成功" in res.text or "模型不存在" in res.text or "完成基本信息的注册" in res.text or "存在" in res.text or "重复" in res.text:
                return {"domain":domain,"res":True,"info":variable_storage.mail}
            if  "Email已经被" in res.text:
                return {"domain": domain, "res": True, "info": "0000001"}
        else:
            res = post_data(session, domain, result, dopost="regok")
            if "成功" in res.text or "模型不存在" in res.text or "完成基本信息的注册" in res.text or "存在" in res.text or "重复" in res.text:
                return {"domain": domain, "res": True, "info": "0000001"}
        message = re.findall('(?<=document.write\()\S+(?="\);)', res.text)[0]
        return {"domain":domain,"res":False,"info":"注册失败：%d--%s"%(res.status_code,message)}
    except ConnectionError as e:
        return {"domain": domain, "res": False, "info": "连接失败"}
    except requests.exceptions.ReadTimeout as e:
        return {"domain": domain, "res": False, "info": "连接超时"}
    except Exception as e:
        if num > 0:
            print("尝试重新注册：" + domain)
            return 注册(domain, num - 1)
        else:
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