# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-07-29 11:00'

from jira import JIRA
import time
import redis


# 生成狐友项目jira的JQL
def generate_jql_list(jira, members):
    jql = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in (MVP_M4后台, 内容分析平台, 超级玛丽, Data_蚁群中心) AND issuetype = Bug AND assignee in ({}) AND status in (Open, 'In Progress', Reopened)".format(
        members)
    issues_list = jira.search_issues(jql, maxResults=1000)

    return issues_list


def jira_daily_defects_2redis():
    username = "autotestsns"
    password = "Welcome2sohu!"
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))

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

    jql_created_in_day = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in (MVP_M4后台, 内容分析平台, 超级玛丽, Data_蚁群中心) AND issuetype = Bug AND created >= {}".format(
        current_date)
    jql_resolved_in_day = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in (MVP_M4后台, 内容分析平台, 超级玛丽, Data_蚁群中心) AND issuetype = Bug AND resolved >= {}".format(
        current_date)
    jql_opening = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in (MVP_M4后台, 内容分析平台, 超级玛丽, Data_蚁群中心) AND issuetype = Bug AND status in (Open, 'In Progress', Reopened) " \
                  "AND assignee in (membersOf(6-spc-pm),membersOf(6-spc-ux),membersOf(6-spc-project),membersOf(6-spc-test),membersOf(6-spc-hydata),membersOf(6-spc-audit),membersOf(6-spc-op),membersOf(6-spc-dm),membersOf(6-spc-cs),membersOf(6-spc-fe),membersOf(6-spc-ios),membersOf(6-spc-android))"

    a_opening = jira.search_issues(jql_opening, maxResults=1000)
    a_created_inday = jira.search_issues(jql_created_in_day, maxResults=1000)
    a_resolved_inday = jira.search_issues(jql_resolved_in_day, maxResults=1000)

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


if '__main__' == __name__:
    jira_daily_defects_2redis()
