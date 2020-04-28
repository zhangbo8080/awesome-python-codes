from spider_function import *
from collections import deque
from prettytable import PrettyTable
from stations import stations
import re
import sys
import io
import time
import urllib.request
import urllib
import gzip
import ssl
import json
header = '车次 出发车站 出发/到达时间 历时 商务座 一等座 二等座 软卧  硬卧 硬座 无座'.split()


if __name__ == "__main__":

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    #     from_st = input('出发地: ' )
    from_st = 'beijing'
#     to_st = input('目的地: ')
    to_st = 'heze'
    from_staion = stations[from_st]
    to_station = stations[to_st]

    date = '2017-01-23'

    url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_staion, to_station
    )

    request = urllib.request.Request(url)

    request.add_header("Accept", "*/*")
    request.add_header("Accept-Language", "zh-CN,zh;q=0.8")
    request.add_header("Cache-Control", "no-cache")
    request.add_header("Connection", "keep-alive")
    request.add_header("Host", "kyfw.12306.cn")
    request.add_header("If-Modified-Since", 0)
    request.add_header("Pragma", "no-cache")
    request.add_header("Referer", "https://kyfw.12306.cn/otn/leftTicket/init")
    request.add_header(
        "User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
    request.add_header("X-Requested-With", "XMLHttpRequest")

    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(request, context=context, timeout=20)
    time.sleep(5)

    data = response.read()

    ungzip(data)
    data_final = data.decode('utf-8')

    r = json.loads(data_final)
    r_len = len(r['data'])

    pt = PrettyTable()
    # 设置每一列的标题
    pt._set_field_names(header)
    for i in range(r_len):
        # if r['data'][i]['queryLeftNewDTO']['station_train_code']=='1303' or r['data'][i]['queryLeftNewDTO']['station_train_code']=='K105' or r['data'][i]['queryLeftNewDTO']['station_train_code']=='K1901' or r['data'][i]['queryLeftNewDTO']['station_train_code']=='K4159':
        #     print(type(r['data'][i]['queryLeftNewDTO']['yz_num']))
        # print（'123'）
        train = [
            # 车次
            r['data'][i]['queryLeftNewDTO']['station_train_code'],
            # 出发、到达站
            '\\'.join([r['data'][i]['queryLeftNewDTO']['from_station_name'], r[
                      'data'][i]['queryLeftNewDTO']['to_station_name']]),
            # 出发、到达时间
            '\\'.join([r['data'][i]['queryLeftNewDTO']['start_time'],
                       r['data'][i]['queryLeftNewDTO']['arrive_time']]),
            # 历时
            r['data'][i]['queryLeftNewDTO']['lishi'],
            # 商务座
            r['data'][i]['queryLeftNewDTO']['swz_num'],
            # 一等坐
            r['data'][i]['queryLeftNewDTO']['zy_num'],
            # 二等坐
            r['data'][i]['queryLeftNewDTO']['ze_num'],
            # 软卧
            r['data'][i]['queryLeftNewDTO']['rw_num'],
            # 软坐
            r['data'][i]['queryLeftNewDTO']['yw_num'],
            # 硬坐
            r['data'][i]['queryLeftNewDTO']['yz_num'],

            # 无座
            r['data'][i]['queryLeftNewDTO']['wz_num']
        ]
        pt.add_row(train)

    print(pt)
