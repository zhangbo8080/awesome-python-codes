# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2021/1/12 15:16'
import os
import time
import threading
import re


def get_connected_devices_list():
    devicesid_list = []
    # 读取设备 id
    readDeviceId = list(os.popen('adb devices').readlines())

    # 正则表达式匹配出 id 信息
    for x in range(len(readDeviceId) - 2):
        deviceId = re.findall(r'^\w*\b', readDeviceId[x + 1])[0]
        devicesid_list.append(deviceId)

    return devicesid_list


def fastboot_traversal(device_id, package_name, running_minutes, throttle):
    fastboot_framework_path = 'C:/Users/bozhang213817/work/code/appCrawler/fastbot/Fastbot_Android/framework.jar'
    fastboot_monkey_path = 'C:/Users/bozhang213817/work/code/appCrawler/fastbot/Fastbot_Android/monkeyq.jar'

    os.system('adb -s {0} push {1} /sdcard'.format(device_id, fastboot_framework_path))
    time.sleep(1)
    os.system('adb -s {0} push {1} /sdcard'.format(device_id, fastboot_monkey_path))
    time.sleep(1)

    fastboot_cmd = 'adb -s {0} shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p {1} --agent robot --running-minutes {2} --throttle {3} -v -v'.format(
        device_id,
        package_name, running_minutes, throttle)

    os.system(fastboot_cmd)


def maxim_traversal(device_id, package_name, running_minutes, throttle):
    maxim_framework_path = 'C:/Users/bozhang213817/work/code/appCrawler/Maxim/framework.jar'
    maxim_monkey_path = 'C:/Users/bozhang213817/work/code/appCrawler/Maxim/monkey.jar'

    os.system('adb -s {0} push {1} /sdcard'.format(device_id, maxim_framework_path))
    time.sleep(1)
    os.system('adb -s {0} push {1} /sdcard'.format(device_id, maxim_monkey_path))
    time.sleep(1)

    maxim_cmd = 'adb -s {0} shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p {1} --uiautomatormix --running-minutes {2} -v -v --throttle {3}'.format(
        device_id,
        package_name, running_minutes, throttle)

    os.system(maxim_cmd)


def traversal_monkey(device_id, package_name, running_minutes, throttle):
    fastboot_traversal(device_id, package_name, running_minutes, throttle)
    time.sleep(2)
    maxim_traversal(device_id, package_name, running_minutes, throttle)


if '__main__' == __name__:
    package_name = 'com.sohu.sohuhy.dev'

    running_minutes = 30

    throttle = 1000

    devicesid_list = get_connected_devices_list()

    thread_list = []
    for device_id in devicesid_list:
        p = threading.Thread(target=traversal_monkey, args=(device_id, package_name, running_minutes, throttle))
        thread_list.append(p)
        p.start()

    for thread in thread_list:
        thread.join()
