# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2020/10/9 17:34'
import testlink


def ini_tlc():
    # 连接test link
    url = "http://testlink.sns.sohuno.com/lib/api/xmlrpc/v1/xmlrpc.php"
    key = "02c4e9d7a24db1e42b315e4ba2821248"
    tlc = testlink.TestlinkAPIClient(url, key)
    return tlc


def getExternalidlist(tlc):
    external_id_list = []
    Cases = tlc.getTestCasesForTestSuite(testsuiteid="159", deep=True, details="simple", getkeywords=True)
    for x in Cases:
        external_id_list.append(x["external_id"])

    return external_id_list


def getTestplanid(tlc, hy_version):
    testplanid = ""
    # 根据项目名称获取项目id
    ProjectID = tlc.getProjectIDByName("hy回归测试用例")
    # 根据项目id获取testplanid
    ProjectTestPlans = tlc.getProjectTestPlans(ProjectID)
    for x in ProjectTestPlans:
        if x["name"] == hy_version:
            testplanid = x["id"]
            break
        else:
            pass
    return testplanid


def assignTestCaseExecutionTask(testpalneid, buildname, external_id_list, tester_list):
    external_id_list_len = len(external_id_list)
    tester_list_len = len(tester_list)
    print(external_id_list_len)
    print(tester_list_len)
    for x in range(0, external_id_list_len):
        testcaseexternalid = external_id_list[x]
        user = tester_list[x % tester_list_len]
        tlc.assignTestCaseExecutionTask(user=user, testplanid=testpalneid, testcaseexternalid=testcaseexternalid,
                                        buildname=buildname)


if __name__ == "__main__":
    hy_version = "v5.9.5"
    tester_list = ["zhangbo", "duhan", "leishuying", "xuqun", "liangzhuojie"]
    tlc = ini_tlc()
    testpalneid = getTestplanid(tlc, hy_version)
    external_id_list = getExternalidlist(tlc)
    assignTestCaseExecutionTask(testpalneid, hy_version, external_id_list, tester_list)
