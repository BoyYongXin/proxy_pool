import time
import sys
sys.path.append("../")
from utils import tools
from db.redisdb import RedisDB
from lxml import etree
import requests
from utils.log import log
from jsonpath import jsonpath
import os
import socket
import os,signal
import time
from storage_module.dection_ping_proxy import check_ip
from retrying import retry
# def write(content_info):
#     f = open('D:\start_get_ip\pid.txt','a',encoding="utf-8")
#     f.write(str(content_info)+"\n")
#     f.close()
# pid=os.getpid()
# print(pid)
# write(pid)
# while True:
#     print(1)
#     time.sleep(34)
redis_0 = RedisDB()
MAX_POOL=400
config = os.path.join('D:\proxy\\' + 'config.conf')


redis_key = tools.get_conf_value(config, 'redis', 'redis_key')
redis_key2 = tools.get_conf_value(config, 'redis', 'redis_key2')
bj_ip = socket.gethostbyname(socket.gethostname())

def retry(attempt):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    print("重试的次数%s" % att)
                    att += 1
        return wrapper
    return decorator

@retry(attempt=100)
def get_proxies():
    api_url = "http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=fadc76e39a074860aaf837b455001f75&returnType=2&count=10"
    api_json=tools.get_json_by_requests(api_url)
    ips=jsonpath(api_json,"$..ip")
    ports=jsonpath(api_json,"$..port")
    if ips and ports:
        for ip,ports in zip(ips,ports):
            proxy=ip+":"+ports
            yield ip,proxy
def ping(ip):
 ''' ping 主备网络 '''
 result = os.system(u"ping {}".format(ip))
 if result == 0:
     return True
 else:
     return False

def save_proxies(ip,ip_addr):
    # proxies = {
    #     "https": "https:" + ip_addr,
    #     "http": "http:" + ip_addr
    # }
    try:
        if ping(ip) == True:
        #if check_ip(ips) == True:
            redis_0.sadd(redis_key,ip_addr)
            redis_0.sadd(redis_key2, ip_addr)

            log.debug("%s成功添加到redis" % ip)
        else:
            log.info("%s代理无效" % ip_addr)

    except Exception as e:

        log.info("出现异常终止")
        sys.exit(0)

if __name__ == "__main__":
    # pid = os.getpid()
    # write(pid)
    while True:
        if redis_0.count(redis_key)>=MAX_POOL:
            time.sleep(15)
            continue
        else:
            ips=get_proxies()
            for ip in ips:
                save_proxies(ip[0],ip[1])