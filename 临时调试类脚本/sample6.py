# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-03-19 16:49'

import requests
import re
import hashlib
import time
import nacos
import yaml

headers = {
    "token": "eyJleHAiOjE1NjA3NjkyMTkyNjYsImlhdCI6MTU1Mjk5MzIxOTI2NiwicHAiOiIxMTA3OTU5OTgxNTY0NjE2NzA0QHNvaHUuY29tIiwidGsiOiJES2g4RG1HREtFMWpSakF3eEJsek1mVG9sNkJCakl4ZSIsInYiOjB9.x44SdfA3bj4UFlzFOBNtd8Zw1I9XS2N0cP9QoU176U8",
    "gid": "x011050101010f36a786548340008eb1c7f7908a80f6",
    "S-PPID": "1107959981564616704@sohu.com",
    "S-PID": "483808037157570432",
    "S-CID": "01472095916057331203",
    "S-VS": "2.2.0",
    "S-AVS": "2.2.0",
    "P-APPID": "110501",

}


# 从nacos上获取需要监控的h5地址
def get_url_from_nacos():
    SERVER_ADDRESSES = "op-test.sns.sohuno.com:80"
    NAMESPACE = "9eae126d-3501-4100-b577-baa2eaeed8ea"

    client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)

    # get config
    data_id = "monitor_h5"
    group = "DEFAULT_GROUP"
    h5_url_list_yaml = client.get_config(data_id, group)

    h5_url_list = yaml.load(h5_url_list_yaml, Loader=yaml.FullLoader)

    return h5_url_list


# 算sig
def getsSig(data_dict, appkey="c90ae28e764d11e69ca0c4346b752337"):
    """

    :param data_dict: 接口参数
    :param appkey: appkey，不同版本key不一样
    :return:
    """
    # print(data_dict)
    sig_string = ""
    for key in sorted(data_dict.keys()):
        if key != 'sig':
            sig_string += key + "=" + str(data_dict[key])
    sig_str = sig_string + appkey
    # print(sig_str)
    sig_md5 = hashlib.md5()
    sig_md5.update(sig_str.encode('utf-8'))
    return sig_md5.hexdigest()


def get_title(Html):
    '''
    用re抽取网页Title
    '''
    pattern = re.compile("<title>(.*)</title>", re.S)
    title_list = pattern.findall(Html)
    if title_list == []:
        title = ''
    else:
        title = title_list[0]

    return title


def dm_login():
    url = "https://dm-ol.sns.sohu.com/dm/api/v1/login"
    get_time = time.time()
    data_init = {
        "token": headers["token"],
        "log_user_id": headers["S-PID"],
        "appid": 330000,
        "flyer": get_time,
        "app_key_vs": "2.2.0",
        "S-PPID": headers["S-PPID"],
        "S-PID": headers["S-PID"],
        "S-CID": headers["S-CID"],
    }

    data = {
        "appid": 330000,
        "flyer": get_time,
        "app_key_vs": "2.2.0",
        "token": headers["token"],
        "sig": getsSig(data_init),
        "log_user_id": headers["S-PID"],

    }
    try:
        response_result = requests.post(url=url, data=data, headers=headers)
    except Exception as err:
        pass


# 内部发送私聊接口
def send_messages(message):
    url = "http://dm-ol.sns.sohu.com/dm/api/internal/v1/notice"
    get_time = time.time()
    data = {
        "token": headers["token"],
        "to_user_id": '240603326599766016',
        "from_user_id": headers["S-PID"],
        "type": 4,
        # "message": message,
        "appid": 10007,
        "flyer": get_time,
        "app_key_vs": "2.2.0",
        "feed_url":"sohuhy://w.sohu.com/cardWall",
        "feed_title":"我要上墙",
        "feed_content":message,
        "feed_original_url":"sohuhy://w.sohu.com/cardWall",
        # "S-PPID": headers["S-PPID"],
        # "S-PID": headers["S-PID"],
        # "S-CID": headers["S-CID"],
    }

    data['sig'] = getsSig(data)

    try:
        # dm_login()
        response_result = requests.post(url=url, data=data, headers=headers)
        print(response_result.content.decode())
    except Exception as err:
        pass


# 内部发送群聊接口
def send_group_messages(message):
    # url = "https://dm-ol.sns.sohu.com/dm/api/v1/group/message"
    url = "http://dm-ol.sns.sohu.com/dm/api/internal/v1/group/notice"
    get_time = time.time()
    data = {
        "group_id": 58817,
        "token": headers["token"],
        "from_user_id": headers["S-PID"],
        "type": 0,
        "message": message,
        "appid": 10007,
        "flyer": get_time,
        "app_key_vs": "2.2.0",
        # "S-PPID": headers["S-PPID"],
        # "S-PID": headers["S-PID"],
        # "S-CID": headers["S-CID"],
    }

    data['sig'] = getsSig(data)

    try:
        # dm_login()
        response_result = requests.post(url=url, data=data, headers=headers)
        print(response_result.content.decode())
    except Exception as err:
        pass


def monitoring_url(url):
    try:
        response_result = requests.get(url, timeout=5)

        if response_result.status_code != 200:
            send_group_messages("H5小伙伴赶紧来看看{}的http的状态码为{}啦!!!".format(url, response_result.status_code))
            send_messages("H5小伙伴赶紧来看看{}的http的状态码为{}啦!!!".format(url, response_result.status_code))
        if get_title(response_result.content.decode()) == "Welcome to nginx!":
            send_group_messages("H5小伙伴赶紧来看看{}出现{}啦!!!".format(url, "Welcome to nginx!"))
            send_messages("H5小伙伴赶紧来看看{}出现{}啦!!!".format(url, "Welcome to nginx!"))
        if get_title(response_result.content.decode()) == "502 Bad Gateway":
            send_group_messages("H5小伙伴赶紧来看看{}出现{}啦!!!".format(url, "502 Bad Gateway"))
            send_messages("H5小伙伴赶紧来看看{}出现{}啦!!!".format(url, "502 Bad Gateway"))

    except Exception as err:
        send_group_messages(err)
        send_messages(err)


if __name__ == "__main__":

    # url = get_url_from_nacos()
    # for x in url:
    #     monitoring_url(x)
    send_messages("为你推荐上墙入口")