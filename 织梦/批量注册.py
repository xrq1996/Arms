import json
from 织梦 import utils
import base64
import requests
from 织梦 import dedecms
from io import BytesIO
from PIL import Image
import traceback
from sys import version_info

###
def base64_api(uname, pwd, img):
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(utils.my_requests(method="post",url="http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


def post_data(session, domain, vcode):
    try:
        "dopost=regbase&step=1&mtype=%E4%B8%AA%E4%BA%BA&mtype=%E4%B8%AA%E4%BA%BA&userid=0000001&uname=0000001&userpwd=qwe123&userpwdok=qwe123&email=ldanche%40protonmail.com&safequestion=0&safeanswer=&sex=&vdcode=bnfl&agree="
        params = {"dopost": "regbase", "step": 1, "mtype": "个人", "mtype": "个人", "userid": "0000001", "uname": "0000001",
                  "userpwd": "qwe123", "userpwdok": "qwe123", "email": "ldanche@protonmail.com", "safequestion": 0,
                  "safeanswer": "", "sex": "", "agree": ""}
        params.update({"vdcode": vcode})
        res = session.get(url=domain + "/member/reg_new.php", params=params,timeout=10)
        if "成功" in res.text or "模型不存在" in res.text or "完成基本信息的注册" in res.text:
            print("%s:注册成功！" % domain)
            return True
        else:
            print("%s:注册失败！" % domain)
    except Exception  as e:
        traceback.print_exc(e)


def 注册(domain, num=5):
    session = requests.session()
    res = session.get(domain + cp_url,timeout=10)
    with open(file="tp.jpg", mode="wb") as fp:
        fp.write(res.content)
    img_path = "tp.jpg"
    img = Image.open(img_path)
    result = base64_api(uname='danche', pwd='qq199605', img=img)
    print(result)
    res = post_data(session, domain, result)
    if res:
        return True
    elif num > 0:
        print("尝试重新注册：" + domain)
        return 注册(domain, num - 1)


if __name__ == "__main__":
    domains = utils.get_lines("./验证注册")
    cp_url = "/include/vdimgck.php"
    for domain in domains:
        try:
            print(domain)
            res = 注册(domain, 3)
            if res:
                with open("注册结果", "a") as f:
                    f.write(domain + '----注册成功\n')
            else:
                with open("注册结果", "a") as f:
                    f.write(domain + '----注册失败\n')
        except Exception as e:
            traceback.print_exc()
            with open("注册结果", "a") as f:
                f.write(domain + '----注册失败\n')
