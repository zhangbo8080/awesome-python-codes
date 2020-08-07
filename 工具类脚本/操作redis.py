# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2018/12/6 15:57'

import redis
from prettyprinter import cpprint


# 写数据
def set_redis(db, key, hash_key, hash_value):
    r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=db)
    r.hset(key, hash_key, hash_value)


# 读数据
def get_redis(db, key):
    r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=db)
    result = r.hgetall(key)
    cpprint(result)


if '__main__' == __name__:
    db = 4  # db=4是日报数据，db=7是需要变更
    key = "2020-08-07"
    hash_key = "bug_daily_fix_rate"
    hash_value = "29%"
    set_redis(db, key, hash_key, hash_value)

