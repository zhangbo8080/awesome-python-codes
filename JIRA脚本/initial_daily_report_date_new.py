# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2020/8/5 10:56'
# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-03-19 16:49'
import time

import nacos
import redis
import yaml
from confluence.client import Confluence


# 将版本对应的主需求的wiki数据初始化到redis存储
def wiki_requirement_details_2redis(pageid_details_dict):
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    r = redis.Redis(host='xxxx', port=xxxx, password="xxx", db=xxx)
    page_id = pageid_details_dict["projects_pageid"]
    r.hset("{}".format(page_id), "projects_pageid", "{}".format(page_id))
    r.hset("{}".format(page_id), "projects_name", "{}".format(pageid_details_dict["projects_name"]))
    r.hset("{}".format(page_id), "projects_testable_version", "{}".format(pageid_details_dict["projects_version"]))
    r.hset("{}".format(page_id), "projects_author", "{}".format(pageid_details_dict["projects_author"]))
    r.hset("{}".format(page_id), "planned_testable_date", "{}".format(pageid_details_dict["planned_testable_date"]))
    r.hset("{}".format(page_id), "actual_testable_date", "{}".format(pageid_details_dict["actual_testable_date"]))
    r.hset("{}".format(page_id), "updated_date", "{}".format(current_date))


# 获取版本需求的wiki数据
def get_wiki_requirement_detail(pageid):
    username = "bozhang213817"
    password = "Benson@009"

    pageid_details_dict = {}

    confluence = Confluence('http://wiki.sohu-inc.com', (username, password))

    content = confluence.get_content_by_id(pageid)

    pageid_details_dict["projects_name"] = content.title
    pageid_details_dict["planned_testable_date"] = "planned_testable_date"
    pageid_details_dict["actual_testable_date"] = "NA"
    pageid_details_dict["projects_version"] = content.version
    pageid_details_dict["projects_pageid"] = pageid
    pageid_details_dict["projects_author"] = content.history.author

    return pageid_details_dict


# 从nacos获取日报配置
def get_daily_report_config():
    SERVER_ADDRESSES = "xxxx"
    NAMESPACE = "xxxa"

    client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)

    # get config
    data_id = "daily_report_config"
    group = "DEFAULT_GROUP"
    daily_report_yaml = client.get_config(data_id, group)

    daily_report_config = yaml.load(daily_report_yaml, Loader=yaml.FullLoader)

    return daily_report_config


if __name__ == "__main__":

    daily_report_config = get_daily_report_config()

    requirement_pageid_list = daily_report_config["requirement_pageid_list"]

    for x in requirement_pageid_list:
        pageid_details_dict = get_wiki_requirement_detail(x)
        wiki_requirement_details_2redis(pageid_details_dict)
