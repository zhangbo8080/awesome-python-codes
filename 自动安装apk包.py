# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2019-10-23 10:33'

from subprocess import call
import os
import time

path = "/Users/mac/Downloads/apks/"

# print(os.listdir(path))

for x in os.listdir(path):
    print("{}-------".format(x), end="")
    call("adb install -r {0}{1}".format(path, x), shell=True)

    time.sleep(3)
