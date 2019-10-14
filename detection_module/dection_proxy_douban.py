# -*- coding: utf-8 -*-
'''
Created on 2019-10-10 01:55
---------
@summary: 验证代理失效性程序
---------
@author: Yongxin_Yang
'''
import sys
sys.path.append("../")
from aiohttp_requests import requests
import time
from db.redisdb import RedisDB
from utils.log import log
from utils import tools
import os
import asyncio

config = os.path.join(os.path.dirname(__file__) + '/../config.conf')
redis_key = tools.get_conf_value(config, 'redis', 'redis_key')

class Detection(object):
    def __init__(self):
        self.redis = RedisDB()
        self.test_url = "https://movie.douban.com/"

    #@tools.debug
    async def get_html(self,root_url,proxy,semaphore):
        try:
            test_proxy = "http://" + proxy
            log.debug("正在测试代理：" + test_proxy)
            async with semaphore:
                response = await requests.get(root_url,proxy=test_proxy,timeout=8)
                html = await response.text()
                return response,html
        except asyncio.TimeoutError as err:
            return [],[]


    #@tools.debug
    async def run(self,content_info):
        semaphore = asyncio.Semaphore(10)
        response ,html = await self.get_html( self.test_url,content_info,semaphore)
        try:
            if html and response:
                if response.status == 200 and '检测到有异常请求' not in html:
                    log.debug("\n" + content_info + " 代理可用")
                else:
                    self.redis.delete_value(redis_key, content_info)
                    log.debug("已清除失效的代理：" + content_info)
            else:
                self.redis.delete_value(redis_key, content_info)
                log.debug("已清除失效的代理：" + content_info)
        except Exception as e:
            self.redis.delete_value(redis_key, content_info)
            log.debug("\n" + content_info + ' 代理请求失败')
            log.debug("已清除失效的代理：" + content_info)

    def doing_main(self):

        task_list = self.redis.get_all(redis_key)
        log.debug('数据库中IP总数{}'.format(len(task_list)))
        tasks = [asyncio.ensure_future(self.run(data)) for data in task_list]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks,timeout=10))

if __name__ == '__main__':

    while True:
        try:
            dt = Detection()
            dt.doing_main()
        except Exception as e:
            print(e)
        finally:
            print('睡眠10秒，再继续验证')

            time.sleep(15)
