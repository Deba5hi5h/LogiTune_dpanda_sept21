import os
import subprocess
import time
from datetime import datetime


class TuneMobileUtils:

    @staticmethod
    def start_emulator(device_name: str):
        """
        Method to start Emulator

        :param device_name:
        :return :
        """
        current_time = str(time.time()).split(".")[1]
        file_name = f"start_emulator_{current_time}.sh"
        port = 5556 if device_name.lower() == "pixel6" else 5554
        f = open(file_name, "w")
        f.writelines(
            ["#!/usr/bin/env bash\n", f"~/Library/Android/sdk/emulator/emulator -avd {device_name} -port {port} -snapshot snapshot"])
        f.close()
        file = f"{os.getcwd()}/{file_name}"
        os.system(f"chmod 755 {file}")
        subprocess.call(['open', '-a', 'Terminal.app', file])
        time.sleep(30)
        os.remove(file)

    @staticmethod
    def stop_emulator(device_name: str):
        """
        Method to stop Emulator

        :param device_name:
        :return :
        """
        port = 5556 if device_name.lower() == "pixel6" else 5554
        time.sleep(5)
        os.system(f'adb -s emulator-{port} emu kill')

    @staticmethod
    def start_appium(port: int = 4723):
        """
        Method to create appium shell script and start Appium

        :param :
        :return :
        """
        current_time = str(time.time()).split(".")[1]
        file_name = f"appium_{current_time}.sh"
        f = open(file_name, "w")
        f.writelines(["#!/usr/bin/env bash\n", f"appium -p {port}"])
        f.close()
        file = f"{os.getcwd()}/{file_name}"
        os.system(f"chmod 755 {file}")
        subprocess.call(['open', '-a', 'Terminal.app', file])
        time.sleep(1)
        os.remove(file)
        print(file_name)

    @staticmethod
    def stop_appium():
        """
        Method to stop Appium

        :param :
        :return :
        """
        os.system('pkill -9 -f appium')

    @staticmethod
    def restart_appium():
        """
        Method to restart Appium

        :param :
        :return :
        """
        TuneMobileUtils.stop_appium()
        TuneMobileUtils.start_appium()
