# -*- coding:utf-8 -*-
# __author__ = 'leizhang'

from jira import JIRA
import os
import datetime
import time
from jinja2 import Environment
from jinja2 import FileSystemLoader
import redis
from collections import deque
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from JIRA脚本.jira_daiy_defect_2redis import jira_daily_defects_2redis
import smtplib
import nacos
import yaml

component_not_supported = "MVP_M4后台, 内容分析平台, 超级玛丽, Data_蚁群中心"


# 从nacos获取日报配置
def get_daily_report_config():
    SERVER_ADDRESSES = "op-test.sns.sohuno.com:80"
    NAMESPACE = "9eae126d-3501-4100-b577-baa2eaeed8ea"

    client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)

    # get config
    data_id = "daily_report_config"
    group = "DEFAULT_GROUP"
    daily_report_yaml = client.get_config(data_id, group)

    daily_report_config = yaml.load(daily_report_yaml, Loader=yaml.FullLoader)

    return daily_report_config


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(mail_content, from_addr, mailto_list, server, team_name):
    # print("trying to send mail by " + server)
    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'狐友测试组 <%s>' % from_addr)
    msg['To'] = ",".join(mailto_list)
    msg['Subject'] = Header(u'狐友Daily Report'.format(team_name), 'utf-8').encode()
    server = smtplib.SMTP(server, 25)
    server.sendmail(from_addr, mailto_list, msg.as_string())
    server.quit()
    # print("send mail successfully")


def get_date_detail_list(old=None):
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # current_date = "2019-08-04"
    date_list = []
    d1 = datetime.datetime.strptime(old, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(current_date, '%Y-%m-%d')
    delta = d2 - d1
    for x in range(delta.days + 1):
        d = datetime.datetime.strptime(old, '%Y-%m-%d')
        delta = datetime.timedelta(days=x)
        date_list.append(str((d + delta).date()))

    date_redis_list = []
    date_redis_list = deque(date_redis_list)
    r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=4)

    for y in date_list:

        if r.hgetall("{}".format(y)):
            date_redis_dict = {}
            date_redis_dict = {
                "date": y,
                "issues_android": r.hget("{}".format(y), "issues_android").decode(),
                "issues_iOS": r.hget("{}".format(y), "issues_iOS").decode(),
                "issues_H5": r.hget("{}".format(y), "issues_H5").decode(),
                "issues_server": r.hget("{}".format(y), "issues_server").decode(),
                "issues_dm": r.hget("{}".format(y), "issues_dm").decode(),
                "issues_OP": r.hget("{}".format(y), "issues_OP").decode(),
                "issues_data": r.hget("{}".format(y), "issues_data").decode(),
                "issues_audit": r.hget("{}".format(y), "issues_audit").decode(),
                "issues_test": r.hget("{}".format(y), "issues_test").decode(),
                "issues_pm": r.hget("{}".format(y), "issues_pm").decode(),
                "issues_ux": r.hget("{}".format(y), "issues_ux").decode(),
                "issues_project": r.hget("{}".format(y), "issues_project").decode(),
            }
            date_redis_list.appendleft(date_redis_dict)

        else:
            pass
    return date_redis_list


def get_date_list(old=None):
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # current_date = "2019-08-04"
    date_list = []
    d1 = datetime.datetime.strptime(old, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(current_date, '%Y-%m-%d')
    delta = d2 - d1
    for x in range(delta.days + 1):
        d = datetime.datetime.strptime(old, '%Y-%m-%d')
        delta = datetime.timedelta(days=x)
        date_list.append(str((d + delta).date()))

    date_redis_list = []
    date_redis_list = deque(date_redis_list)
    r = redis.Redis(host='mb.y.redis.sohucs.com', port=22939, password="b87418ff6e92b4db923e71b3eeaf9d7c", db=4)

    for y in date_list:

        if r.hgetall("{}".format(y)):
            date_redis_dict = {}
            date_redis_dict = {
                "date": y,
                "a_opening": r.hget("{}".format(y), "a_opening").decode(),
                "a_created_inday": r.hget("{}".format(y), "a_created_inday").decode(),
                "a_resolved_inday": r.hget("{}".format(y), "a_resolved_inday").decode(),
            }
            date_redis_list.appendleft(date_redis_dict)

        else:
            pass

    return date_redis_list


def format_date(date):
    return date.split("T")[0]


def order_by_priority(issues_list):
    priority_five_list = []
    priority_four_list = []
    priority_thress_list = []
    priority_other_list = []

    for x in issues_list:
        # print(x.fields.priority.name)
        if x.fields.priority.name == "５级":
            priority_five_list.append(x)
        elif x.fields.priority.name == "４级":
            priority_four_list.append(x)
        elif x.fields.priority.name == "3级":
            priority_thress_list.append(x)
        else:
            priority_other_list.append(x)

    return priority_five_list + priority_four_list + priority_thress_list + priority_other_list


# 生成狐友项目jira的JQL
def generate_jql(jira, members):
    jql = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component not in ({0}) AND issuetype = Bug AND assignee in ({1}) AND status in (Open, 'In Progress', Reopened)".format(
        component_not_supported, members)
    issues_list = jira.search_issues(jql, maxResults=1000)
    issues_order_by_priority = order_by_priority(issues_list)
    return issues_order_by_priority


def main(version, date_start):
    username = "autotestsns"
    password = "Welcome2sohu!"
    # current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))

    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)), keep_trailing_newline=True)
    env.filters['datetime'] = format_date
    template = env.get_template('mailcontent_daily_report.html')
    defect_date_count = get_date_list(date_start)
    defect_date_detail = get_date_detail_list(date_start)
    output = template.render(board_name="狐友{}".format(version),
                             issues_android=generate_jql(jira, 'membersOf(6-spc-android)'),
                             issues_iOS=generate_jql(jira, 'membersOf(6-spc-ios)'),
                             issues_server=generate_jql(jira, 'membersOf(6-spc-cs)'),
                             issues_OP=generate_jql(jira, 'membersOf(6-spc-op)'),
                             issues_H5=generate_jql(jira, 'membersOf(6-spc-fe)'),
                             issues_data=generate_jql(jira, 'membersOf(6-spc-hydata)'),
                             issues_audit=generate_jql(jira, 'membersOf(6-spc-audit)'),
                             issues_dm=generate_jql(jira, 'membersOf(6-spc-dm)'),
                             issues_pm=generate_jql(jira, 'membersOf(6-spc-project)'),
                             issues_test=generate_jql(jira, 'membersOf(6-spc-test)'),
                             issues_ux=generate_jql(jira, 'membersOf(6-spc-ux)'),
                             issues_project=generate_jql(jira, 'membersOf(6-spc-pm)'),
                             defect_date_count=defect_date_count,
                             defect_date_detail=defect_date_detail
                             )

    with open("C:/Users/bozhang213817/Desktop/daily_bug.html", "w", encoding="utf-8") as f:
        f.write(output)

    # try:
    #     send_mail(output, "autotestsns@sohu-inc.com", ["bozhang213817@sohu-inc.com"], "mail.mtpc.sohu.com", "狐友Daily Report")
    # except Exception as e:
    #     print("hit exception, when send mail")
    #     print(e)


if '__main__' == __name__:
    daily_report_config = get_daily_report_config()

    version = daily_report_config["version"]

    date_start = daily_report_config["date_start"].strftime("%Y-%m-%d")

    jira_daily_defects_2redis()

    main(version, date_start)
