import logging
import os
from multiprocessing.dummy import Pool as ThreadPool
import time
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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

def ping(ip):
    ''' ping 主备网络 '''
    result = os.system(u"ping {}".format(ip))
    if result == 0:
        return True
    else:
        return False

