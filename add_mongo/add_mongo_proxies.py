from jsonpath import jsonpath
import json
from utils.log import log
from pymongo import MongoClient
import requests
import pymongo
import time
conn = MongoClient('localhost', 27017)
client = conn["proxy_save"]
db = client["proxy"]
# api_url = 'http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pro=0&city=0&yys=0&port=1&pack=30957&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=0&regions=110000'
#api_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=fadc76e39a074860aaf837b455001f75&orderno=YZ201811210433Ic2MjU&returnType=1&count=1'
def write_url(data):
    try:
        #proxies = requests.get(api_url).text
        proxies = data

        # if '请更换地区重新生成api链接' in proxies:
        #     db.insert({"proxy": {}})
        #     return ''
        # proxies = proxies.replace("\r\n","")
        # log.debug(proxies)
        if proxies:
            db.remove()
            db.insert({"proxy": proxies})
        else:
            db.remove()
            log.debug("获取ip失败")
            db.insert({"proxy": {}})
    except Exception as e:
        db.remove()
        db.insert({"proxy": {}})
        log.debug(e)



if __name__ == "__main__":
    while True:
        result = write_url()
        time.sleep(90)