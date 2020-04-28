from spider_function import *
from collections import deque

import re, sys, io,time
import urllib.request
import urllib
import gzip  

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    url = 'http://www.dy2018.com/'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, timeout=10)
    time.sleep(2)
    data = response.read().decode('gbk')
    ungzip(data)

#     print(data)

#     pattern = re.compile('<span>(.*?)</span>', re.S)
#     print("2016新片精品")
#     pattern = re.compile(r'2016新片精品.*?title=\".*?\">(.*?)</a>.*?迅雷电影资源')
    pattern = re.compile(r'title=\"(.*?)\">', re.S)
    items = pattern.findall(data)
#     print(items)
    count_num = 0
    for item in items:
        count_num += 1
        if count_num < 16:
            if count_num ==1:
                print ("---------------2016新片精品---------------")
            print (item)
        elif count_num > 30 and count_num <46:
            if count_num ==31:
                print()
                print ("---------------迅雷电影资源---------------")
            print (item)           
        elif count_num > 60 and count_num <76:
            if count_num ==61:
                print()
                print ("---------------华语电视剧---------------")
            print (item) 
        elif count_num > 90 and count_num <106:
            if count_num ==91:
                print()
                print ("---------------欧美电视剧---------------")
            print (item) 

