from common import utils
from common import variable_storage
import requests
from PIL import Image
import traceback

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
    except Exception as e:
        traceback.print_exc()


def 注册(domain, num=5):
    session = requests.session()
    res = session.get(domain + variable_storage.dede_vc_url,timeout=10)
    with open(file="tp.jpg", mode="wb") as fp:
        fp.write(res.content)
    img_path = "tp.jpg"
    img = Image.open(img_path)
    result = utils.base64_api(uname='danche', pwd='qq199605', img=img)
    print(result)
    res = post_data(session, domain, result)
    if res:
        return True
    elif num > 0:
        print("尝试重新注册：" + domain)
        return 注册(domain, num - 1)

def main():
    while True:
        # get domain
        domain = ""
        res = 注册(domain=domain)
        #结果入库



if __name__ == "__main__":
    domains = utils.get_lines("./验证注册")
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