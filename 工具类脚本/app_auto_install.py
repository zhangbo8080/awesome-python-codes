# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2021/3/2 14:08'
import jenkins
import requests
import os
import re
import threading
import time


# 从jenkins上获取最新的apk地址
def get_apks(JENKINS_URL, JOB_NAME, app_prefix):
    server = jenkins.Jenkins(JENKINS_URL)
    job_info = server.get_job_info(JOB_NAME)

    build_info = server.get_build_info(JOB_NAME, job_info["lastStableBuild"]["number"])

    artifacts = build_info["artifacts"]
    url = build_info["url"]
    for x in artifacts:
        if app_prefix in x["fileName"] and ".apk" in x["fileName"]:
            return url + "artifact/" + x["fileName"]


# 下载apk文件到本地
def download_apks(url):
    print(url)
    file_name = str(url).split("/")[-1]
    file_path = "C:/Users/bozhang213817/Desktop/{0}".format(file_name)
    r = requests.get(url)
    with open(file_path, "wb") as code:
        code.write(r.content)

    print(file_path)
    return file_path


def get_connected_devices_list():
    devicesid_list = []
    # 读取设备 id
    readDeviceId = list(os.popen('adb devices').readlines())

    # 正则表达式匹配出 id 信息
    for x in range(len(readDeviceId) - 2):
        deviceId = re.findall(r'^\w*\b', readDeviceId[x + 1])[0]
        devicesid_list.append(deviceId)

    return devicesid_list


def check_devices_status(device_id):
    devices_status_info = os.popen('adb -s {0} shell dumpsys window policy'.format(device_id)).readlines()

    for x in devices_status_info:
        if 'mScreenOnEarly=false' in x:
            os.system('adb -s {0} shell input keyevent 26'.format(device_id))
            break
        else:
            pass


def get_adb_install(device_id, file_path):
    check_devices_status(device_id)
    time.sleep(1)
    os.system('adb -s {0} install -r {1}'.format(device_id, file_path))


if '__main__' == __name__:

    JENKINS_URL = 'http://10.2.11.50:8070/jenkins/view/hy_android/'
    JOB_NAME = "hy_android_dev"
    app_prefix = "Test_release"

    apk_url = get_apks(JENKINS_URL, JOB_NAME, app_prefix)

    file_path = download_apks(apk_url)

    devicesid_list = get_connected_devices_list()

    thread_list = []

    for device_id in devicesid_list:
        p = threading.Thread(target=get_adb_install, args=(device_id, file_path))
        thread_list.append(p)
        p.start()

    for thread in thread_list:
        thread.join()
