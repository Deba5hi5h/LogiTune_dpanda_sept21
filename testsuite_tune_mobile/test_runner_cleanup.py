import os
import time

from apps.tune_mobile.tune_mobile_utils import TuneMobileUtils

appium = TuneMobileUtils()
appium.stop_appium()

directory = os.getcwd() + "/netshare"

i = 6
while i > 0:
    result = os.system("umount " + directory)
    if result == 0:
        break
    i -= 1
    time.sleep(10)