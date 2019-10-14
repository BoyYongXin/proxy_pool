# -*- coding: utf-8 -*-
'''
Created on 2019-10-10 01:55
---------
@summary: 启动代理接口程序
---------
@author: Yongxin_Yang
'''
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import gen
import os
import json
from utils import tools

import random
from db.redisdb import RedisDB
redis = RedisDB()
config = os.path.join(os.path.dirname(__file__) + '/../config.conf')
redis_key = tools.get_conf_value(config, 'redis', 'redis_key2')

class IndexHandler(tornado.web.RequestHandler):
    async def get(self):
        num = int(self.get_argument('num'))#获取url参数
        total_count = redis.sget_count(table=redis_key)
        ip_pools = redis.sget(table=redis_key, count=total_count)
        ip_Random = []  # 定义随机数列表
        random.shuffle(ip_pools)  # 打乱列表顺序
        ip_Random = ip_pools[0:num]  # 截取打乱后的前num个值，赋值给新列表iRandom
        if ip_Random:
            result = {'result':'获取ip成功','get_count':len(ip_Random),'proxy':ip_Random}
        else:
            result = {'result': '未知原因，请联系开发人员','get_count':len(ip_Random), 'proxy': []}

        self.write(result)

class Application(tornado.web.Application): #创建 Application 对象， 定义 setting 和 URL 映射规则
    def __init__(self):

        handlers = [
            (r"/GetProxy", IndexHandler),
        ]
        settings = dict(
                debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)  # 将参数设置传递到父类 Application中
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())  # 传递 Application 对象，封装成 HTTPServer 对象
    http_server.listen(8888,address="192.168.80.60")  # 启动 HTTPServer 监听，实际上    HTTPServer 继承自 TCPServer，是在TCPServer 中启动 listen Socket 端口
    tornado.ioloop.IOLoop.instance().start()#获取全局IOLoop单例，启动IOLoop大循环
