# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-03-29 16:08'

from jira import JIRA
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(mail_content, from_addr, mailto_list, server, team_name):
    print("trying to send mail by " + server)
    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'狐友测试组 <%s>' % from_addr)
    msg['To'] = ",".join(mailto_list)
    msg['Subject'] = Header(u'{}3天还未解决的BUG列表'.format(team_name), 'utf-8').encode()
    server = smtplib.SMTP(server, 25)
    server.sendmail(from_addr, mailto_list, msg.as_string())
    server.quit()
    print("send mail successfully")


def format_date(date):
    return date.split("T")[0]


def check_3d_before_bug(team_name, team_list, mailto_list):
    username = "autotestsns"
    password = "Welcome2sohu!"
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))
    bug_3d_before = "project in (HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH) " \
                    "AND issuetype = Bug " \
                    "AND assignee not in (wenyuyin)" \
                    "AND status in (Open, 'In Progress', Reopened) " \
                    "AND created <= -3d " \
                    "AND assignee in ({})".format(team_list)
    issues_bug_3d_before = jira.search_issues(bug_3d_before, maxResults=1000)

    if issues_bug_3d_before:

        env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)), keep_trailing_newline=True)
        env.filters['datetime'] = format_date
        template = env.get_template('mailcontent_3d.html')
        output = template.render(board_name=team_name, issues_3d=issues_bug_3d_before)

        try:
            send_mail(output, "autotestsns@sohu-inc.com", mailto_list, "mail.mtpc.sohu.com", team_name)
        except Exception as e:
            print("hit exception, when send mail")
            print(e)
    else:
        pass


if '__main__' == __name__:

    team_list = [
        [
            "H5组",
            "membersOf(6-spc-fe)",
            ["xuefengliu@sohu-inc.com", "bozhang213817@sohu-inc.com"]
        ],
        [
            "Android组",
            "membersOf(6-spc-android)",
            ["jinfengchen@sohu-inc.com", "bozhang213817@sohu-inc.com"]
        ],
        [
            "iOS组",
            "membersOf(6-spc-ios)",
            ["kaijin@sohu-inc.com", "bozhang213817@sohu-inc.com"]

        ],
        [
            "核心服务组",
            "membersOf(6-spc-cs)",
            ["guoqingwang@sohu-inc.com", "wenyuyin@sohu-inc.com", "bozhang213817@sohu-inc.com"]
        ],
        [
            "后台组",
            "membersOf(6-spc-op)",
            ["wenzou@sohu-inc.com", "wenyuyin@sohu-inc.com", "bozhang213817@sohu-inc.com"]
        ],
        [
            "私信组",
            "membersOf(6-spc-dm)",
            ["xiaoyuzhao211729@sohu-inc.com", "hughyu@sohu-inc.com", "wenyuyin@sohu-inc.com",
             "bozhang213817@sohu-inc.com"]
        ],
        [
            "测试组",
            "membersOf(6-spc-test)",
            ["bozhang213817@sohu-inc.com"]
        ],
        [
            "产品组",
            "membersOf(6-spc-project)",
            ["zhijiehao@sohu-inc.com", "xiaoyuechen@sohu-inc.com", "jingtinghan@sohu-inc.com", "zhijiehao@sohu-inc.com",
             "chunyangju@sohu-inc.com", "rongquantian213935@sohu-inc.com", "junnazhang213334@sohu-inc.com",
             "yangzhang214392@sohu-inc.com", "bozhang213817@sohu-inc.com"]
        ],
        [
            "数据组",
            "membersOf(6-spc-hydata)",
            ["leisong@sohu-inc.com", "bozhang213817@sohu-inc.com"]
        ],
        [
            "审核组",
            "membersOf(6-spc-audit)",
            ["hughyu@sohu-inc.com", "wenyuyin@sohu-inc.com", "bozhang213817@sohu-inc.com"]
        ],

    ]

    for x in team_list:
        check_3d_before_bug(x[0], x[1], x[2])
