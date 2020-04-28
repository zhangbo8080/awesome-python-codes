from spider_function import *
from collections import deque

import re, sys, io
import urllib.request
import urllib
import gzip  

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    url = 'http://www.dygang.com/'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, timeout=5)
    data = response.read().decode('gbk')
    ungzip(data)

#     print(data)

#     pattern = re.compile('<span>(.*?)</span>', re.S)
#     print("2016新片精品")
#     pattern = re.compile(r'2016新片精品.*?title=\".*?\">(.*?)</a>.*?迅雷电影资源')
    pattern = re.compile(r'class=\"c2\">(.*?)</a>', re.S)
    items = pattern.findall(data)
#     print(items)
    count_num = 0
    for item in items:
        count_num += 1
        if count_num < 17:
            if count_num ==1:
                print ("---------------最新电影---------------")
            print (item)
        elif count_num > 16 and count_num <33:
            if count_num ==17:
                print()
                print ("---------------最新电视剧---------------")
            print (item)           
        