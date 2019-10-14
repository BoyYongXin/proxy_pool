import os
import time
import sys
sys.path.append("../")
from utils import tools
from utils.log import log
from db.redisdb import RedisDB
def monitor_proxies():
    redis_0 = RedisDB()
    config = os.path.join(os.path.dirname(__file__) + '/../config.conf')
    redis_key = tools.get_conf_value(config, 'redis', 'redis_key')
    redis_key2 = tools.get_conf_value(config, 'redis', 'redis_key2')
    sum = redis_0.count(redis_key)
    sum2 = redis_0.count(redis_key2)

    log.debug("douban当前redis库中剩余ip总数：%d"%sum)
    log.debug("weibo当前redis库中剩余ip总数：%d" % sum2)
if __name__ == "__main__":
	while True:	
		monitor_proxies()
		time.sleep(30)