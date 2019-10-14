import socket
import sys
sys.path.append("../")
from db.redisdb import RedisDB
from utils.log import log
from utils import tools
import os
import time
import aiohttp
import asyncio

TEST_URL="https://movie.douban.com/"
config = os.path.join(os.path.dirname(__file__) + '/../config.conf')
redis_key = tools.get_conf_value(config, 'redis', 'redis_key')
BATCH_SIZE=50
class Detection(object):
    def __init__(self):
        self.redis=RedisDB()

    async def detection_proxy(self, proxy, semaphore):
        async with semaphore:
            con = aiohttp.TCPConnector(verify_ssl=False,family=socket.AF_INET,limit=60)
            async with aiohttp.ClientSession(connector=con) as session:
                try:
                    test_proxy="http://"+proxy
                    log.debug("正在测试代理："+ test_proxy)
                    async with session.get(TEST_URL,proxy=test_proxy,timeout=7) as response:
                        html = await response.text()
                        if response.status==200 and '检测到有异常请求' not in html:
                            log.debug("\n"+proxy+" 代理可用")
                        else:
                            self.redis.delete_value(redis_key,proxy)
                            log.debug("已清除失效的代理："+proxy)
                except Exception as e:
                    self.redis.delete_value(redis_key, proxy)
                    log.debug("\n"+proxy+' 代理请求失败')
                    log.debug("已清除失效的代理：" + proxy)
    def run(self):
        try:
            proxies=self.redis.get_all(redis_key)
            # semaphore = asyncio.Semaphore(15)
            # loop= asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_SIZE):
                test_proxies = proxies[i:i + BATCH_SIZE]
                self.main(test_proxies)
                # task = [self.detection_proxy(proxy, semaphore) for proxy in test_proxies]
                # loop.run_until_complete(asyncio.wait(task))
        except Exception as e :
            log.debug("测试发生错误",e.args)
    def main(self,test_proxies):
        semaphore = asyncio.Semaphore(5)
        loop = asyncio.get_event_loop()
        task = [self.detection_proxy(proxy, semaphore) for proxy in test_proxies]
        loop.run_until_complete(asyncio.wait(task))
if __name__ == "__main__":
    while True:
        try:
            dt = Detection()
            dt.run()
            time.sleep(10)
        except Exception as e:
            print(e)
            time.sleep(10)
