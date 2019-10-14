# -*- coding: utf-8 -*-
'''
Created on 2019-10-10 01:55
---------
@summary: 启动获取代理程序
---------
@author: Yongxin_Yang
'''
import sys
sys.path.append("../")
from utils import tools
from db.redisdb import RedisDB
from utils.log import log
from jsonpath import jsonpath
import socket
import logging
import os
from multiprocessing.dummy import Pool as ThreadPool
import time
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    api_url = "http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=afadc76e39a074860aaf837b455001f75&returnType=2&count=10"
    api_json=tools.get_json_by_requests(api_url)
    ips=jsonpath(api_json,"$..ip")
    ports=jsonpath(api_json,"$..port")
    if ips and ports:
        ips_list = []
        for ip,ports in zip(ips,ports):
            proxy=ip+":"+ports
            ip_info = {'ip':ip,'proxy':proxy}
            ips_list.append(ip_info)
        return ips_list
            #yield ip,proxy
def save_proxies(ips_list):
    try:
        check_ip(ips_list)
    except Exception as e:
        log.info("出现异常终止")
        sys.exit(0)
def check_ip(ips):
    pool = ThreadPool(10)
    results = pool.map(ping,ips)  # 该语句将不同的url传给各自的线程，并把执行后结果返回到results中
    success=results.count(True)
    faild = results.count(False)
    logging.info(
        '''
        ping数据成功%s条
        ping数据失败%s条
       '''
        %(success,faild))
    pool.close()
    pool.join()

def ping(ip_info):
    ''' ping 主备网络 '''
    ip = ip_info['ip']
    proxy = ip_info['proxy']
    result = os.system(u"ping {}".format(ip))
    if result == 0:
        redis_0.sadd(redis_key, proxy)
        redis_0.sadd(redis_key2, proxy)

        log.debug("%s成功添加到redis" % ip)
        return True
    else:
        log.info("%s代理无效" % proxy)
        return False


if __name__ == "__main__":
    while True:
        try:
            if redis_0.count(redis_key)>=MAX_POOL:
                time.sleep(5)
                continue
            else:
                ips_list=get_proxies()
                save_proxies(ips_list)
        except:
            time.sleep(5)