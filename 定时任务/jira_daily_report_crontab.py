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
import smtplib
import nacos
import yaml


def jira_daily_defects_2redis():
    username = "autotestsns"
    password = "Welcome2sohu!"
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))

    # Android组JQL
    jql_android = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-android)) AND status in (Open, 'In Progress', Reopened)"
    issues_android = jira.search_issues(jql_android, maxResults=1000)

    # iOS组JQL
    jql_iOS = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-ios)) AND status in (Open, 'In Progress', Reopened)"
    issues_iOS = jira.search_issues(jql_iOS, maxResults=1000)

    # H5组JQL
    jql_H5 = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-fe)) AND status in (Open, 'In Progress', Reopened)"
    issues_H5 = jira.search_issues(jql_H5, maxResults=1000)

    # 核心服务组JQL
    jql_Server = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-cs)) AND status in (Open, 'In Progress', Reopened)"
    issues_server = jira.search_issues(jql_Server, maxResults=1000)

    # 私信组JQL
    jql_dm = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-dm)) AND status in (Open, 'In Progress', Reopened)"
    issues_dm = jira.search_issues(jql_dm, maxResults=1000)

    # OP组JQL
    jql_OP = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-op)) AND status in (Open, 'In Progress', Reopened)"
    issues_OP = jira.search_issues(jql_OP, maxResults=1000)

    # 数据组JQL
    jql_data = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-hydata)) AND status in (Open, 'In Progress', Reopened)"
    issues_data = jira.search_issues(jql_data, maxResults=1000)

    # 审核组JQL
    jql_audit = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-audit)) AND status in (Open, 'In Progress', Reopened)"
    issues_audit = jira.search_issues(jql_audit, maxResults=1000)

    # 测试组JQL
    jql_test = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-test)) AND status in (Open, 'In Progress', Reopened)"
    issues_test = jira.search_issues(jql_test, maxResults=1000)

    # 产品组JQL
    jql_pm = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-project)) AND status in (Open, 'In Progress', Reopened)"
    issues_pm = jira.search_issues(jql_pm, maxResults=1000)

    # 设计组JQL
    jql_ux = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-ux)) AND status in (Open, 'In Progress', Reopened)"
    issues_ux = jira.search_issues(jql_ux, maxResults=1000)

    # 项目组JQL
    jql_project = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in (membersOf(6-spc-pm)) AND status in (Open, 'In Progress', Reopened)"
    issues_project = jira.search_issues(jql_project, maxResults=1000)

    jql_created_in_day = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND created >= {}".format(
        current_date)
    jql_resolved_in_day = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND resolved >= {}".format(
        current_date)
    jql_opening = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND status in (Open, 'In Progress', Reopened) " \
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
    jql = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) AND component != MVP_M4后台 AND issuetype = Bug AND assignee in ({}) AND status in (Open, 'In Progress', Reopened)".format(
        members)
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

    # with open("/Users/mac/Downloads/daily_bug.html", "w", encoding="utf-8") as f:
    #     f.write(output)

    try:
        send_mail(output, "autotestsns@sohu-inc.com", ["bozhang213817@sohu-inc.com"], "mail.mtpc.sohu.com",
                  "狐友Daily Report")
    except Exception as e:
        print("hit exception, when send mail")
        print(e)


if '__main__' == __name__:
    daily_report_config = get_daily_report_config()

    version = daily_report_config["version"]

    date_start = daily_report_config["date_start"].strftime("%Y-%m-%d")

    jira_daily_defects_2redis()

    main(version, date_start)
