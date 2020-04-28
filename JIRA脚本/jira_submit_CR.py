# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019/12/12 19:31'

from jira import JIRA


def submit_cr(project=None, summary=None):
    username = "bozhang213817"
    password = "Benson@007"
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))
    # HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH
    issue_dict = {'project': project, 'issuetype': '测试任务', 'summary': summary,
                  'assignee': {'name': 'yannawang210897'}}

    jira.create_issue(fields=issue_dict)

    # issue = jira.issue('HUYOU-4238')
    # print(dir(issue))
    # print(dir(issue.fields))
    # print(issue.fields.project)
    # print(issue.fields.issuetype)
    # print(issue.fields.priority)
    # print(issue.fields.reporter)
    # print(issue.fields.summary)


if '__main__' == __name__:
    # HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH

    project_list = ["HUYOUANDROID","HUYOUIOS"]

    summary = "链接类大小卡片优化 - UI验收"

    for project in project_list:
        submit_cr(project, summary)
