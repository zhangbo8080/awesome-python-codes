# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2020/8/6 17:59'
import time
import subprocess
import os

text = "去哪儿旅行15周年"

for x in range(1, 2000):
    # cmd_screenshot = "adb shell /system/bin/screencap -p /sdcard/431703023178329984/{}.png".format(x)
    #
    # subprocess.Popen(cmd_screenshot, stderr=subprocess.PIPE, shell=False)
    #
    # cmd_swipe = "adb shell input swipe 340 865 370 202"
    #
    # subprocess.Popen(cmd_swipe, stderr=subprocess.PIPE, shell=False)
    #
    # time.sleep(1)

    # 切换adb输入法
    # os.system('adb shell ime set com.android.adbkeyboard/.AdbIME')

    #切换至搜狗输入法
    # os.system('adb shell ime set com.sohu.inputmethod.sogou /.SogouIME')
    # adb shell ime set com.sohu.inputmethod.sogou.xiaomi/.SogouIME
    #输入内容
    os.system('adb shell am broadcast -a ADB_INPUT_TEXT --es msg {}'.format(text))
    os.system('adb shell input keyevent  66')
    # time.sleep(0.5)



