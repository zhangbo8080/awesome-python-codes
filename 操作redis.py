# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2018/12/6 15:57'

import redis
from prettyprinter import cpprint

r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=14)
# r.hset("18611134450_headers", 'token',"eyJleHAiOjE1NTIyOTMyMzQwMzUsImlhdCI6MTU0NDUxNzIzNDAzNSwicHAiOiI4NzAxODkyMjU5NjkzODEzNzZAc29odS5jb20iLCJ0ayI6IjNrMnZPaFlkWERmMHRpR1NoWG12QWVnZmlsa2RSTHFIIiwidiI6MH0.oYhWKos-z77tMPDGpZXJcdIYYHK5uu697aCrvL-q2Mo")
# r.hset("18611134450_headers", 'gid',"x011050101010dc565515ec36000080b5f6ec03f780f")
# headers = {}
# headers['token'] = r.hget("18611134450_headers", 'token').decode()
# headers['gid'] = r.hget("18611134450_headers", 'gid').decode()
#
# cpprint(headers)


r.set("test", "test")
value_test = r.get("test").decode()
print(value_test)

