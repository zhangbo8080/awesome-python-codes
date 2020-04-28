# -*- coding:utf-8 -*-
# __author__ = 'zhangbo'

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


def send_mail(mail_content, from_addr, mailto_list, password, server):
    print("trying to send mail by " + server)
    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'狐友测试组 <%s>' % from_addr)
    msg['To'] = ",".join(mailto_list)
    msg['Subject'] = Header(u'Jira 日报 - 狐友MVP已修复的BUG数', 'utf-8').encode()
    server = smtplib.SMTP(server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, mailto_list, msg.as_string())
    server.quit()
    print("send mail successfully")

def format_date(date):
    return date.split("T")[0]

def main():
    username = "autotestsns"
    password = "Welcome2sohu!"
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))

    jql_resolved_bug="project in (SNSHH, HUYOUIOS, HUYOUANDROID, HUYOU) AND issuetype = Bug AND status = Resolved"
    issues_resolved_bug = jira.search_issues(jql_resolved_bug, maxResults=1000)
    reporter_list=[]
    for x in issues_resolved_bug:
        reporter_list.append(x.fields.reporter)

    import pandas as pd
    result = pd.value_counts(reporter_list)
    print(result)

    # result_report_dic= dict(result)


    # mailto_list = ["spctest@sohu-inc.com","spcpm@sohu-inc.com","spc-project@sohu-inc.com","spcux@sohu-inc.com",]
    # mailto_list = ["bozhang213817@sohu-inc.com",]

    # env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)), keep_trailing_newline=True)
    # env.filters['datetime'] = format_date
    # template = env.get_template('mailcontent.html')
    # output = template.render(board_name="狐友MVP需要复测的BUG列表", resolved = result_report_dic)

    #
    # print(output)
    # with open("/Users/mac/Downloads/resolved_bug.html","w") as f:
    #     f.write(output)
    # try:
    #      send_mail(output, "autotestsns@sohu-inc.com", mailto_list, "Welcome2sohu!", "transport.mail.sohu-inc.com")
    # except Exception as e:
    #     print("hit exception, when send mail")
    #     print(e)


if '__main__' == __name__:
    main()