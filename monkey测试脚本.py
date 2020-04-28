# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 下午2:37
# @Author  : ZhaoWei
import os


# 获取连接的android手机的udid
def checkDevicesPlatform():
    """
    :return: 根据当前系统的平台获取devices id或者udid
    """
    cmd = 'adb devices'
    try:
        results_android = os.popen(cmd, "r")
        results_lines = results_android.readlines()
        # print(results_lines)
        if len(results_lines) == 2:
            y = []
            # print(y)
            return y
        else:
            l = []
            for x in range(len(results_lines)):
                if x + 1 < len(results_lines) - 1:
                    results_line = results_lines[x + 1].replace('\n', '').split('\tdevice')[0]
                    l.append(results_line)
            # print(l)
            return l
    except Exception as e:
        print(e, '未返回device_id')


# monkey脚本
def monkey_script(udid):
    """

    :param udid: 测试设备的udid
    :return: 制定设备的monkey脚本
    """
    cmd = "adb -s {0} shell monkey -c android.intent.category.LAUNCHER -c android.intent.category.MONKEY -c \
    android.intent.category.DEFAULT -p com.sohu.sohuhy --ignore-crashes --ignore-timeouts \
    --ignore-security-exceptions --ignore-native-crashes --monitor-native-crashes --pct-touch\
     40 --pct-syskeys 20 --pct-motion 19 --pct-nav 20 --pct-appswitch 1 -s 87631 -v-v -v \
     --hprof --throttle 1000 100000 > D:/monkey_log_{0}.txt 2>&1".format(udid)

    return cmd


if __name__ == "__main__":
    import time
    print(time.ctime())
    udid_list = checkDevicesPlatform()
    print(udid_list)
    if udid_list:
        for x in udid_list:
            os.popen(monkey_script(x))
    else:
        print("请检查连接的设备！！！")
