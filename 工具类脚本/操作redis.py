# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2018/12/6 15:57'


import redis

current_date = "2020-08-06"

r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=4)

# 写数据
r.hset("{}".format(current_date), "android_dev", "{}".format("100%"))
# 读数据
# r.hget("{}".format(y), "a_created_inday").decode()

# r.set("test", "test")
# r.get("test").decode()
