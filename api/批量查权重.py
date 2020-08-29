import requests
import json
import traceback
from common import utils

my_key = "b899b8e88d183a23a5206f8dcf169bec"

def bash_select_weight():
    domains = list(utils.get_lines("查权重"))
    ress = {}
    domains_g = utils.group_by_list(domains, 50)
    for domains in domains_g:
        try:
            aizhan_api = "https://apistore.aizhan.com/baidurank/siteinfos/%s?domains=%s"
            res = utils.my_requests(aizhan_api%(my_key,"|".join(domains).replace("https://","").replace("http://","")))
            for data in json.loads(res.text)["data"]["success"]:
                ress.update({data["domain"]:data["pc_br"]})
        except Exception as e:
            traceback.print_exc()
    ress = sorted(ress.items(), key=lambda d: d[1], reverse=True)
    with open(file="./res/权重",mode="a") as fp:
        for res in ress:
            fp.write("\nd%s|%s"%(res[0], res[1]))


if __name__ == '__main__':
    bash_select_weight()git config core. excludesfile .gitignore