from spider_function import *
from collections import deque

import re
import urllib.request
import urllib
import gzip  

if __name__ == "__main__":
    queue = deque()
    visited = set()
    url = 'http://www.solarbao.com'  # 入口页面, 可以换成别的
    fileinit()  # 指定爬取数据的存储位置，并且爬之前先清空之间的数据
    
    queue.append(url)
    cnt = 0

    while queue:
        url = queue.popleft()  # 队首元素出队
        visited |= {url}  # 标记为已访问
        print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
        cnt += 1
    #执行爬url方法            
        data_final = getHtml(url)
     
      # 按指定正则规则爬数据并保存在指定文件中
        if data_final != False:
            temp_data = spider_1(data_final)
               
    # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
            for x in temp_data:
                if 'html' in x and x not in visited:
                    queue.append(x)
                    print('加入队列 --->  ' + x)
            
            # 按指定正则规则爬数据并保存在指定文件中
            temp_data2 = spider_2(data_final)
            temp_data3 = spider_3(data_final)
            temp_data4 = spider_4(data_final)
        else:
            continue       
    print('抓取结束！！！')
