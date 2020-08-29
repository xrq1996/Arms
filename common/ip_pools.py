from common import utils


class IPPools():
    def __init__(self,api,min_num,max_num):
        self.api = api
        self.min_num = min_num
        self.max_num = max_num
        self.ips = []


    # def invoke