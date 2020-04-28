from collections import deque
import re
import urllib.request
import urllib
import gzip  
import random

def getUA():
    uaList = [
    'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+TencentTraveler)',
    'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+2.0.50727;+.NET+CLR+3.0.4506.2152;+.NET+CLR+3.5.30729)',
    'Mozilla/5.0+(Windows+NT+5.1)+AppleWebKit/537.1+(KHTML,+like+Gecko)+Chrome/21.0.1180.89+Safari/537.1',
    'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1)',
    'Mozilla/5.0+(Windows+NT+6.1;+rv:11.0)+Gecko/20100101+Firefox/11.0',
    'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+SV1)',
    'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)',
    'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+KB974489)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    ]
    ua = random.choice(uaList)
    return ua

def getHtml(url):
    #httplib.HTTPConnection.debuglevel = 1
    request = urllib.request.Request(url)
    #accessCookie = cookielib.CookieJar()
    request.add_header("Accept", "text/html, application/xhtml+xml, */*")
#     request.add_header('Upgrade-Insecure-Requests', 1)
    request.add_header("User-Agent", getUA())
#     request.add_header('Cache-Control', 'max-age=0')
    request.add_header("Accept-Language", "en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3")
#     request.add_header("Accept-Encoding", "gzip, deflate, sdch")
    request.add_header("Connection","Keep-Alive")
    try:
        response = urllib.request.urlopen(request,timeout=2)
#         if 'html' not in response.getheader('Content-Type'):
#             continue
        data = response.read()

        ungzip(data)

        return data.decode('utf-8')
    except:
        print('抓取<--- '+url+'时出现异常，请检查原因！！！')
        return False

def fileinit():
    with open('D:/spider_test.txt', 'w') as f:
        f.write("开始爬啦！！！")
        f.write("\n")

    
    with open('D:/spider_test2.txt', 'w') as f2:
        f2.write("开始爬啦！！！")
        f2.write("\n")

    
    with open('D:/spider_test3.txt', 'w') as f3:
        f3.write("开始爬啦！！！")
        f3.write("\n")
    
    with open('D:/spider_test4.txt', 'w') as f4:
        f4.write("开始爬啦！！！")
        f4.write("\n")

def ungzip(data):
    try:  # 尝试解压
#         print('正在解压.....')
        data = gzip.decompress(data)
#         print('解压完毕!') 
    except:
        pass
#         print('未经压缩, 无需解压')
    return data

def spider_1(data):
    # 正则
    linkre = re.compile('href=\"(http\:\/\/www\.solarbao.+?)\"')   
    temp_data = set(linkre.findall(data))
    with open('D:/spider_test.txt', 'a') as f:
        f.write("\n")
        for x in temp_data:
            f.write(x)
            f.write("\n")
    return temp_data    

def spider_2(data):
    # 正则
    linkre = re.compile('\".+?\.css\"')   
    temp_data = set(linkre.findall(data))
    with open('D:/spider_test2.txt', 'a') as f:
        f.write("\n")
        for x in temp_data:
            f.write(x)
            f.write("\n")
    return temp_data    

def spider_3(data):
    # 正则
    linkre = re.compile('\"\/.+?\.js\"')   
    temp_data = set(linkre.findall(data))
    with open('D:/spider_test3.txt', 'a') as f:
        f.write("\n")
        for x in temp_data:
            f.write(x)
            f.write("\n")
    return temp_data

def spider_4(data):
    # 正则
    linkre = re.compile('src=\"\/.+?\.jpg\"|src=\"\/.+?\.png\"')   
    temp_data = set(linkre.findall(data))
    with open('D:/spider_test4.txt', 'a') as f:
        f.write("\n")
        for x in temp_data:
            f.write(x)
            f.write("\n")
    return temp_data  

   