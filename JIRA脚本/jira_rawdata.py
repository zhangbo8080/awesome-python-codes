# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019/12/18 19:33'

from jira import JIRA
import time
import xlwt


def generate_jira_rawdata(jql):
    username = "bozhang213817"
    password = "Benson@007"

    jira = JIRA('http://jira.sohuno.com/', basic_auth=(username, password))

    issues = jira.search_issues(jql, maxResults=1000)

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Sheet")

    name_list = ["项目", "关键字", "主题", "是否功能缺失", "问题类型", "状态", "优先级", "解决结果", "经办人", "报告人", "创建时间", "创建日期", "解决时间", "修复周期",
                 "影响版本", "模块", "BUG分类"]

    name_column = 0

    for x in name_list:
        sheet.write(0, name_column, x)  # sheet.write(行,列,内容)
        name_column = name_column + 1

    row = 1
    column = 0

    for issue in issues:
        # 项目
        sheet.write(row, column, str(issue.fields.project))
        # print(issue.fields.project)

        # 关键字
        sheet.write(row, column + 1, str(issue.key))
        # print(issue.key)

        # 主题
        sheet.write(row, column + 2, str(issue.fields.summary))
        # print(issue.fields.summary)

        # 是否功能缺失
        if "qs-" in str(issue.fields.summary):
            sheet.write(row, column + 3, "Yes")
        else:
            sheet.write(row, column + 3, "No")

        # 问题类型
        sheet.write(row, column + 4, str(issue.fields.issuetype))
        # print(issue.fields.issuetype)

        # 状态
        sheet.write(row, column + 5, str(issue.fields.status))
        # print(issue.fields.status)

        # 优先级
        sheet.write(row, column + 6, str(issue.fields.priority))
        # print(issue.fields.priority)

        # 解决结果
        if issue.fields.resolution:
            sheet.write(row, column + 7, str(issue.fields.resolution))
        else:
            sheet.write(row, column + 7, "未解决")
        # print(issue.fields.resolution)

        # 经办人
        sheet.write(row, column + 8, str(issue.fields.assignee))
        # print(issue.fields.assignee)

        # 报告人
        sheet.write(row, column + 9, str(issue.fields.reporter))
        # print(issue.fields.reporter)

        # 创建时间
        sheet.write(row, column + 10, str(issue.fields.created))
        # print(issue.fields.created)

        # 创建日期
        sheet.write(row, column + 11, str(issue.fields.created.split('T')[0]))
        # print(issue.fields.created.split('T')[0])

        # 解决时间
        if issue.fields.resolutiondate:
            sheet.write(row, column + 12, str(issue.fields.resolutiondate))
        else:
            sheet.write(row, column + 12, " ")
        # print(issue.fields.resolutiondate)

        # 修复周期
        if issue.fields.resolutiondate:
            created_timeArray = time.strptime(issue.fields.created.split('.')[0], "%Y-%m-%dT%H:%M:%S")
            created_timeStamp = int(time.mktime(created_timeArray))
            resolutiondate_timeArray = time.strptime(issue.fields.resolutiondate.split('.')[0], "%Y-%m-%dT%H:%M:%S")
            resolutiondate_timeStamp = int(time.mktime(resolutiondate_timeArray))
            sheet.write(row, column + 13, ('%.2f' % ((resolutiondate_timeStamp - created_timeStamp) / 86400)))
        else:
            sheet.write(row, column + 13, " ")

        # print('%.2f' % ((resolutiondate_timeStamp - created_timeStamp) / 86400))

        # 影响版本
        sheet.write(row, column + 14, str(issue.fields.versions[0]))
        # print(issue.fields.versions[0])

        # 模块
        sheet.write(row, column + 15, str(issue.fields.components[0]))
        # print(issue.fields.components[0])

        # BUG分类
        sheet.write(row, column + 16, str(issue.fields.customfield_11203))


        row = row + 1

    workbook.save(r'D:\jirarawdata.xls')


if '__main__' == __name__:
    # HUYOUANDROID, HUYOUIOS, HUYOU, SNSHH

    jql = 'project in (HUYOUIOS, HUYOUANDROID, SNSHH, HUYOU) AND issuetype = Bug AND component not in (MVP_M4后台, 内容分析平台) AND created >= 2020-4-3 AND created <= 2020-12-29'

    generate_jira_rawdata(jql)
