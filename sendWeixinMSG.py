import os
import json
from subprocess import call

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=882c197f-5396-426f-8461-3aab19e56da8"

ua = "Content-Type:application/json"

file_path = "D:/sample.json"

# content_json = {
#     "msgtype": "text",
#     "text": {
#         "content": "hello world"
#     }
# }

# content_json = {
#     "msgtype": "news",
#     "news": {
#         "articles": [
#             {
#                 "title": "测试推图片",
#                 "description": "这里放描述",
#                 "url": "www.sohu.com",
#                 "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
#             }
#         ]
#     }
# }

content_json ={
    "msgtype": "markdown",
    "markdown": {
        "content": "测试markdown<font color=\"warning\">xxx例</font>，请相关同事注意。\n \
         类型:<font color=\"comment\">用户反馈</font> \n \
         普通用户反馈:<font color=\"comment\">ssss例</font> \n \
         VIP用户反馈:<font color=\"comment\">1sss例</font>"
    }
}

with open(file_path, "w") as f:
    f.write(json.dumps(content_json))

call(
    u'curl "{0}" -H "{1}" -d@"{2}"'.format(url, ua, file_path))

os.remove(file_path)
