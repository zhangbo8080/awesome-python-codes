# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-03-28 15:37'

from jira import JIRA


def main(start_data):
    username = "autotestsns"
    password = "Welcome2sohu!"
    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))

    jql_bug_count = "project in (SNSHH, HUYOUIOS, HUYOUANDROID, HUYOU, SNSMY,SNSM4) " \
                    "AND issuetype = Bug AND status = Closed " \
                    "AND resolution = Fixed " \
                    "AND reporter in (membersOf(6-spc-test))" \
                    "AND created >= {} " \
                    "ORDER BY createdDate DESC".format(start_data)
    # , 超级玛丽, MVP_M4后台
    issues_resolved_bug = jira.search_issues(jql_bug_count, maxResults=1000)
    reporter_list = []
    for x in issues_resolved_bug:
        reporter_list.append(x.fields.reporter)

    import pandas as pd
    result = pd.value_counts(reporter_list)
    print(result)


if '__main__' == __name__:

    start_data = "2021-02-25"
    print("当前版本有效BUG数")
    main(start_data)
