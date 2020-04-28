from spider_function import *
from collections import deque
from prettytable import PrettyTable
from connectDB_spider import *
import re
import urllib.request
import urllib
import gzip
header = '产品名称 预计年化收益 产品单价 锁定期 '.split()

if __name__ == "__main__":

    sql = "SELECT pro_id FROM yangguang_chonggou.www_product GROUP BY pro_id limit 100"
    conn, cur = connDB()
    exeQuery(cur, sql)
    pro_all = cur.fetchall()
    connClose(conn, cur)
    data_queue = []
    for row, in pro_all:
        url = "http://cswww.solarbao.com/licai/" + str(row) + ".html"

        data = getHtml(url)

    #     linkre = re.compile('新品中心</a>&nbsp;>&nbsp;<h1>(.*?)</h1>')
        linkre = re.compile(
            '新品中心.*?<h1>(.*?)</h1>.*?预期年化收益.*?fixed_income">(.*?)</span>.*?产品单价.*?transfer-detail-b-fm ">(.*?)</span>.*? 锁定期限.*?transfer-detail-b-fm ">(.*?)</span>', re.S)
    #     linkre = re.compile('美橙(.*?)7')
        temp_data = linkre.findall(data)
        if temp_data != []:
            #             print(temp_data)
            data_queue.append(temp_data)
    pt = PrettyTable()
    # 设置每一列的标题
    pt._set_field_names(header)
#     print(data_queue)

    for x in data_queue:
        #         pro_id=[x[0][0],x[0][1],x[0][2],x[0][3]]
        pt.add_row(x[0])
    print(pt)
