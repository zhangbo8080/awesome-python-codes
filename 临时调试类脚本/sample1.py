import time
import subprocess

for x in range(1, 150):
    cmd_screenshot = "adb shell /system/bin/screencap -p /sdcard/431703023178329984/{}.png".format(x)

    subprocess.Popen(cmd_screenshot, stderr=subprocess.PIPE, shell=False)

    cmd_swipe = "adb shell input swipe 340 865 370 202"

    subprocess.Popen(cmd_swipe, stderr=subprocess.PIPE, shell=False)

    time.sleep(1)


