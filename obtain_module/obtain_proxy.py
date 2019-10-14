import os
import sys
sys.path.append("../")
from utils import tools
from db.redisdb import RedisDB
import random
# [redis]
# # ip:port; 多个逗号分隔
# ip_ports = 192.168.1.103:6379
# user_pass =
# # 默认 0 到 15 共16个数据库
# db = 0
# redis_key = proxy_pools:proxy1
import sys
sys.path.append("../")
import os
from utils import tools
from db.redisdb import RedisDB
import random
# [redis]
# # ip:port; 多个逗号分隔
# ip_ports = 192.168.1.103:6379
# user_pass =
# # 默认 0 到 15 共16个数据库
# db = 0
# redis_key = proxy_pools:proxy1
config = os.path.join(os.path.dirname(__file__) + '/../config.conf')
redis_key = tools.get_conf_value(config, 'redis', 'redis_key')
def random_proxy():
    try:
        redis=RedisDB()
        ip_pools=redis.sget(table=redis_key,count=1)
        proxy=random.choice(ip_pools)
        proxies = {
            "http": proxy,
            "https": proxy,
        }
    except Exception as e:
        print(e)
        proxies={}
    return proxies
print(random_proxy())
