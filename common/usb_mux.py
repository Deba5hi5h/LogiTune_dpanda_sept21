import os
import time

import brainstem
#for easy access to error constants
import psutil
from brainstem import discover
from brainstem.result import Result

from common.platform_helper import get_custom_platform
from extentreport.report import Report
from base import global_variables
import argparse

MUX_SERIAL = 0xD8DDABB2
USBC_COMMON = 0
PORT_WIN10 = 0
PORT_MAC11 = 1
PORT_WIN11 = 2
PORT_MAC12 = 3

cswitch = brainstem.stem.USBCSwitch()
parser = argparse.ArgumentParser()
parser.add_argument("-p","--platform", help="platform os")
args = parser.parse_args()
os_name = args.platform

def get_port_number(os_name):
    if str(os_name).upper() == "WIN10":
        return PORT_WIN10
    elif str(os_name).upper() == "WIN11":
        return PORT_WIN11
    elif str(os_name).upper() == "MAC11":
        return PORT_MAC11
    elif str(os_name).upper() == "MAC12":
        return PORT_MAC12
    else:
        print(f'Platform {os_name} not found')
        raise Exception(f'Platform {os_name} not found')

if get_custom_platform() == "windows":
    for proc in psutil.process_iter():
        if 'StemTool.exe' in proc.name():
            os.system("Taskkill /IM StemTool.exe")
            time.sleep(5)
else:
    os.system('pkill StemTool')

port_number = get_port_number(os_name)
result = cswitch.discoverAndConnect(brainstem.link.Spec.USB, serial_number=MUX_SERIAL)
if result == Result.NO_ERROR:
    err = cswitch.usb.setPortDisable(USBC_COMMON)
    if port_number in (1, 3):
        e = cswitch.usb.setCableFlip(0, 0)
    else:
        e = cswitch.usb.setCableFlip(0, 1)
    err = cswitch.mux.setChannel(port_number)
    err = cswitch.usb.setPortEnable(USBC_COMMON)
    err = cswitch.usb.setSuperSpeedDataDisable(0)
    err = cswitch.usb.setAltModeConfig(0, 0)
    # err = cswitch.usb.setHiSpeedDataDisable(2)
    # err = cswitch.mux.setChannel(port_number)
    if err != Result.NO_ERROR:
        print("Error %d encountered changing the channel." % err)
        raise Exception('Error switching to platform')
        exit(1)
    else:
        print(f"Switched to platform channel {os_name}")
else:
    print('Could not find a module.')
    raise Exception('Could not find a module.')
cswitch.disconnect()


