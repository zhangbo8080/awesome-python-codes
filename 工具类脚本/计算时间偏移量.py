# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-01-16 11:44'

import datetime

time_now = datetime.datetime.now()

min_switch=26000


print(min_switch)
time = (time_now + datetime.timedelta(minutes=min_switch)).strftime("%Y/%m/%d %H:%M:%S")
print(time)