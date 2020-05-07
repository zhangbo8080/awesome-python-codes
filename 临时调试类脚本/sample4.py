# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2018/8/31 16:55'


import hashlib
from prettyprinter import cpprint
import requests
import time
import redis

r = redis.Redis(host='sb.y.redis.sohucs.com', port=25939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=2)

headers = {}

headers['token'] = r.hget('18611134450_headers', 'token').decode()
headers['gid'] = r.hget('18611134450_headers', 'gid').decode()
headers['S-PID'] = r.hget('18611134450_headers', 'S-PID').decode()
headers['S-PPID'] = r.hget('18611134450_headers', 'S-PPID').decode()
headers['S-CID'] = r.hget('18611134450_headers', 'S-CID').decode()
headers['S-VS'] = r.hget('18611134450_headers', 'S-VS').decode()
headers['S-AVS'] = r.hget('18611134450_headers', 'S-AVS').decode()
headers['P-APPID'] = r.hget('18611134450_headers', 'P-APPID').decode()

# headers[
#     'token'] = "eyJleHAiOjE1NDQ5MjgyNDg1ODQsImlhdCI6MTUzNzE1MjI0ODU4NCwicHAiOiI4NjQ3NTUyNjkyOTE0OTk1MjBAc29odS5jb20iLCJ0ayI6IjA5U0tFakpFY2QwREJVNmRUNjBUTGRqdTNkRVlZV2dPIiwidiI6MH0.GgKmLoveEZY7zs66fTZRUF86z-CFdpIj49a_BmpgPcA"
# headers['gid'] = "x011050101010dc43930bf0410000ce8697a88d39b4e"
# headers['S-PID'] = "243454772382894464"
# headers['S-PPID'] = "864755269291499520@sohu.com"
# headers['S-CID'] = "01362286224884543488"
# headers['S-VS'] = "1.12.0"
# headers['S-AVS'] = "1.12.0"
# headers['P-APPID'] = "110501"



def getsSig(data_dict, appkey):
    sig_string = ""
    for key in sorted(data_dict.keys()):
        if key != 'sig':
            sig_string += key + "=" + str(data_dict[key])
    sig_str = sig_string + appkey
    sig_md5 = hashlib.md5()
    sig_md5.update(sig_str.encode('utf-8'))
    return sig_md5.hexdigest()


appkey = "0303BP42w1100M0F"

flyer = time.time()
timestamp = int(time.time()) * 1000

data_dict = {

    'log_user_id': headers["S-PID"],
    'profile_user_id': headers["S-PID"],
    "type": 1,
    "appid": "330000",
    "flyer": flyer,
    "app_key_vs": "1.12.0",
    "token": headers["token"],
}

additional_dict = {

    "S-PPID": headers["S-PPID"],
    "S-CID": headers["S-CID"],
    "S-PID": headers["S-PID"],
}

sig_dict = dict(data_dict, **additional_dict)

sig = getsSig(sig_dict, appkey)

# 测试环境URL
# url = "http://10.10.87.62:8080/330000/v6/feeds/dynamic"

# 线上环境URL
url = "http://10.16.13.101:8080/330000/v6/share/sns/to_outside"

data_dict["sig"] = sig

a = requests.post(url, data=data_dict, headers=headers)
# b = a.json()["data"]["feedList"]
cpprint(a.json())
# for x in b:
#     if x["userTogetherFeedCount"]:
#         print("userTogetherFeedCount =", x["userTogetherFeedCount"], "togetherUserName =", x["togetherUserName"])
