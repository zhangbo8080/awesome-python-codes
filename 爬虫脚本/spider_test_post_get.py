from spider_function import *
from collections import deque

import re
import sys
import io
import time
import urllib.request
import urllib.parse
import gzip
import json
import http.cookiejar
import hashlib


def post(url, value):
    postdata = urllib.parse.urlencode(value).encode('UTF8')
    request = urllib.request.Request(url, postdata)
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')


def get(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')

if __name__ == "__main__":
    #     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    #loginurl = 'http://msapi.t.sohu.com/username/check'
    
    url = 'https://item.jd.com/1029441334.html'
    m = hashlib.md5()
    m.update('appid=18611134450ct=12345600appid=tttt'.encode('utf-8'))
    sig = m.hexdigest()     
    #cookies = http.cookiejar.CookieJar()
    values = {
        'user_name': '18611134450',
        'ct': '12345600',
        'appid':'tttt',
        'sig':sig
    }
   
    # postdata = urllib.parse.urlencode(value).encode('UTF8')
#     print(postdata)
    #opener = urllib.request.build_opener(
        #urllib.request.HTTPCookieProcessor(cookies))
    #data = post(loginurl,values)
    data = get(url)
    print(data)
    #data_json = json.loads(data)
    #print(data_json)
    #print(data_json["message"], data_json["errorCode"])
