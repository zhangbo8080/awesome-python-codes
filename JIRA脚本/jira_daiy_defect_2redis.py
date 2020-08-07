# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-07-29 11:00'
import nacos
import yaml
from jira import JIRA
import time
import redis
import threading
import jenkins
from datetime import datetime
from confluence.client import Confluence


# 生成狐友项目jira的JQL
def generate_jql_list(jira, members):
    jql = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND issuetype = Bug AND assignee in ({1}) AND status in (Open, 'In Progress', Reopened)".format(
        component_not_supported, members)
    issues_list = jira.search_issues(jql, maxResults=1000)

    return issues_list


def jira_daily_defects_2redis():
    username = "autotestsns"
    password = "Welcome2sohu!"

    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # 初始化jira
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))
    # 从nacos获取日报配置
    daily_report_config = get_nacos_config()
    date_start = daily_report_config["date_start"]
    # Android组JQL
    issues_android = generate_jql_list(jira, 'membersOf(6-spc-android)')

    # iOS组JQL
    issues_iOS = generate_jql_list(jira, 'membersOf(6-spc-ios)')

    # H5组JQL
    issues_H5 = generate_jql_list(jira, 'membersOf(6-spc-fe)')

    # 核心服务组JQL
    issues_server = generate_jql_list(jira, 'membersOf(6-spc-cs)')

    # 私信组JQL
    issues_dm = generate_jql_list(jira, 'membersOf(6-spc-dm)')

    # OP组JQL
    issues_OP = generate_jql_list(jira, 'membersOf(6-spc-op)')

    # 数据组JQL
    issues_data = generate_jql_list(jira, 'membersOf(6-spc-hydata)')

    # 审核组JQL
    issues_audit = generate_jql_list(jira, 'membersOf(6-spc-audit)')

    # 测试组JQL
    issues_test = generate_jql_list(jira, 'membersOf(6-spc-test)')

    # 产品组JQL
    issues_pm = generate_jql_list(jira, 'membersOf(6-spc-project)')

    # 设计组JQL
    issues_ux = generate_jql_list(jira, 'membersOf(6-spc-ux)')

    # 项目组JQL
    issues_project = generate_jql_list(jira, 'membersOf(6-spc-pm)')

    jql_created_in_day = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND issuetype = Bug AND created >= {1}".format(
        component_not_supported, current_date)
    jql_resolved_in_day = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND issuetype = Bug AND resolved >= {1}".format(
        component_not_supported, current_date)
    jql_opening = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND issuetype = Bug AND status in (Open, 'In Progress', Reopened) " \
                  "AND assignee in (membersOf(6-spc-pm),membersOf(6-spc-ux),membersOf(6-spc-project),membersOf(6-spc-test),membersOf(6-spc-hydata),membersOf(6-spc-audit),membersOf(6-spc-op),membersOf(6-spc-dm),membersOf(6-spc-cs),membersOf(6-spc-fe),membersOf(6-spc-ios),membersOf(6-spc-android))".format(
        component_not_supported)

    a_opening = jira.search_issues(jql_opening, maxResults=1000)
    a_created_inday = jira.search_issues(jql_created_in_day, maxResults=1000)
    a_resolved_inday = jira.search_issues(jql_resolved_in_day, maxResults=1000)
    # bug日清率
    jql_daily_all_bug = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND issuetype = Bug AND created >={1}".format(
        component_not_supported, current_date)
    current_day_created_bugs = jira.search_issues(jql_daily_all_bug,
                                                  maxResults=1000)
    current_day_created_bug_nums = len(current_day_created_bugs)
    jql_daily_resolved_bug = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND issuetype = Bug AND created >={1} AND Resolved >={1}".format(
        component_not_supported, current_date)
    current_day_resolved_bugs = jira.search_issues(jql_daily_resolved_bug,
                                                   maxResults=1000)
    current_day_resolved_bug_nums = len(current_day_resolved_bugs)

    if current_day_created_bug_nums:

        daily_resolved_rate = '{:.0f}%'.format(
            current_day_resolved_bug_nums / current_day_created_bug_nums * 100)  # 计算日清率
    else:
        daily_resolved_rate = "NA"

    # bug关闭率
    jql_allbug = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND created >={1}".format(
        component_not_supported, date_start)
    jql_closedbug = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND created >={1} AND status = Closed".format(
        component_not_supported, date_start)

    allbug_list = jira.search_issues(jql_allbug, maxResults=1000)
    closebug_list = jira.search_issues(jql_closedbug, maxResults=1000)

    closed_rate = cal_closed_rate(closebug_list, allbug_list)

    # 存redis
    r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=4)

    r.hset("{}".format(current_date), "a_opening", "{}".format(len(a_opening)))
    r.hset("{}".format(current_date), "a_created_inday", "{}".format(len(a_created_inday)))
    r.hset("{}".format(current_date), "a_resolved_inday", "{}".format(len(a_resolved_inday)))
    r.hset("{}".format(current_date), "issues_android", "{}".format(len(issues_android)))
    r.hset("{}".format(current_date), "issues_iOS", "{}".format(len(issues_iOS)))
    r.hset("{}".format(current_date), "issues_H5", "{}".format(len(issues_H5)))
    r.hset("{}".format(current_date), "issues_server", "{}".format(len(issues_server)))
    r.hset("{}".format(current_date), "issues_dm", "{}".format(len(issues_dm)))
    r.hset("{}".format(current_date), "issues_OP", "{}".format(len(issues_OP)))
    r.hset("{}".format(current_date), "issues_data", "{}".format(len(issues_data)))
    r.hset("{}".format(current_date), "issues_audit", "{}".format(len(issues_audit)))
    r.hset("{}".format(current_date), "issues_test", "{}".format(len(issues_test)))
    r.hset("{}".format(current_date), "issues_pm", "{}".format(len(issues_pm)))
    r.hset("{}".format(current_date), "issues_ux", "{}".format(len(issues_ux)))
    r.hset("{}".format(current_date), "issues_project", "{}".format(len(issues_project)))
    r.hset("{}".format(current_date), "bug_close_rate", "{}".format("%.0f%%" % (closed_rate * 100)))
    r.hset("{}".format(current_date), "bug_daily_fix_rate", "{}".format(daily_resolved_rate))


# 计算百分比
def cal_closed_rate(current_item, all_item):
    return len(current_item) / len(all_item)


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)
        try:
            return self.result
        except Exception:
            return None


def success_rate_of_jobs(date, url, job_name):
    """
    :param date: data形式为2020-08-04
    :return: 返回一个百分数
    """
    user_name = 'admin'
    pass_word = 'admin'
    server = jenkins.Jenkins(url=url, username=user_name, password=pass_word)

    last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
    temp0 = server.get_build_info(job_name, last_build_number)['timestamp']
    last_build_date = time.strftime("%Y-%m-%d", time.localtime(temp0 // 1000))
    total_build_count = success_build_count = 0
    if date > last_build_date:  # 输入的日期比最近构建的日期大，也就是晚于最近构建的日期，说明没有打包
        return None
    week_day = datetime.strptime(date, "%Y-%m-%d").weekday()  # 0-6依次代表周一到周日
    if week_day in [5, 6]:  # 如果是周六周日，就不统计
        return None
    for i in range(last_build_number, 0, -1):
        temp = server.get_build_info(job_name, i)['timestamp']
        build_date = time.strftime("%Y-%m-%d", time.localtime(temp // 1000))
        build_result = server.get_build_info(job_name, i)['result']
        if build_date == date and build_result != "ABORTED":
            total_build_count += 1
            if build_result == "SUCCESS":
                success_build_count += 1
        elif build_date < date:
            break

    try:
        rate = round(success_build_count / total_build_count, 2)
    except:
        return None
    else:
        return str(rate * 100) + "%"


def result(date):
    url_android = 'http://10.2.11.50:8070/jenkins/view/hy_android/'  # Android Dev Jenkins
    url_ios = 'http://10.2.11.54:8080/jenkins/'  # iOS Dev Jenkins

    rate, android_rate, ios_rate = {}, {}, {}

    android = MyThread(success_rate_of_jobs, (date, url_android, 'hy_android_dev'))
    android.start()
    ios = MyThread(success_rate_of_jobs, (date, url_ios, 'sohuHy_Dev_new'))
    ios.start()

    ios_rate['ios_dev'] = ios.get_result()
    android_rate['android_dev'] = android.get_result()
    rate[date] = [android_rate, ios_rate]
    return rate


def jenkins_CI_success_rate_2redis():
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # current_date = "2020-07-29"
    jinkens_result = result(current_date)

    r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=4)

    android_dev_rate = jinkens_result[current_date][0]["android_dev"]
    ios_dev_dev_rate = jinkens_result[current_date][1]["ios_dev"]

    if android_dev_rate:
        r.hset("{}".format(current_date), "android_dev", "{}%".format(android_dev_rate.split(".")[0]))
    else:
        r.hset("{}".format(current_date), "android_dev", "未打包")
    if ios_dev_dev_rate:
        r.hset("{}".format(current_date), "ios_dev", "{}%".format(ios_dev_dev_rate.split(".")[0]))
    else:
        r.hset("{}".format(current_date), "ios_dev", "未打包")


def get_nacos_config():
    # 从nacos获取日报配置
    SERVER_ADDRESSES = "op-test.sns.sohuno.com:80"
    NAMESPACE = "9eae126d-3501-4100-b577-baa2eaeed8ea"

    client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)

    # get config
    data_id = "daily_report_config"
    group = "DEFAULT_GROUP"
    daily_report_yaml = client.get_config(data_id, group)

    daily_report_config = yaml.load(daily_report_yaml, Loader=yaml.FullLoader)

    return daily_report_config


def wiki_requirement_changed_times_2redis():
    # username = "bozhang213817"
    # password = "Benson@009"
    username = "autotestsns"
    password = "Welcome2sohu!"
    # 从nacos获取日报配置

    daily_report_config = get_nacos_config()

    requirement_pageid_list = daily_report_config["requirement_pageid_list"]

    # 更新需求的版本号
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=7)
    for page_id in requirement_pageid_list:
        # 获取版本的wiki数据

        confluence = Confluence('http://wiki.sohu-inc.com', (username, password))
        content = confluence.get_content_by_id(page_id)
        r.hset("{}".format(page_id), "projects_version_latest", "{}".format(content.version))


if '__main__' == __name__:
    component_not_supported = "MVP_M4后台, 内容分析平台, 超级玛丽, Data_蚁群中心"
    jira_daily_defects_2redis()
    jenkins_CI_success_rate_2redis()
    wiki_requirement_changed_times_2redis()
