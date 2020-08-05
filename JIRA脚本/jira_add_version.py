# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-01-21 16:20'


from jira import JIRA


def is_not_server(add_version):
    username = "autotestsns"
    password = "Welcome2sohu!"
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))
    jql_open_bug = "project in (SNSHH, HUYOUIOS, HUYOUANDROID) AND issuetype = Bug AND status in (Open, 'In Progress', Reopened, 延期处理) ORDER BY createdDate DESC"
    issues_open_bug = jira.search_issues(jql_open_bug, maxResults=1000)

    for x in issues_open_bug:
        try:
            x.update(versions=[{"add": {'name': add_version}}])
            print(x.fields.versions)
        except Exception as err:
            print(err)


def is_server(add_version):
    username = "autotestsns"
    password = "Welcome2sohu!"
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))
    jql_open_bug = "project in (HUYOU) AND component in (MVP_服务端, MVP_OP后台, MVP_数据后台, MVP_M4后台) AND issuetype = Bug AND status in (Open, 'In Progress', Reopened, 延期处理) ORDER BY createdDate DESC"
    issues_open_bug = jira.search_issues(jql_open_bug, maxResults=1000)

    for x in issues_open_bug:
        try:
            x.update(versions=[{"add": {'name': add_version}}])
            print(x.fields.versions)
        except Exception as err:
            print(err)


if '__main__' == __name__:
    add_version = 'v5.8.0'
    is_not_server(add_version)
    is_server(add_version)
