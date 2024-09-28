import asyncio
import re
import time
import os
import platform

import psutil
from subprocess import Popen, check_output

from apps.DriverOpenApp import GetDriverForOpenApp
from base.base_ui import UIBase
from base import global_variables
from base.listener import CustomListener
from common.platform_helper import get_custom_platform, get_current_system_version
from extentreport.report import Report
from locators.app_locators import WinAppLocators

from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.common.by import By

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(root_dir, "WinApp")


class BluetoothControl(UIBase):
    """
    A class contains methods to control bluetooth connection, pairing, discovery, on/off
    See READ.ME for installing bluetooth tools for Windows/macOS in advanced
    """

    def bluetooth_connect(self, device_mac: str) -> None:
        """
        Method to do bluetooth connection
        :param device_mac: bt address of device
        :return none
        """
        Report.logInfo(f"Connect {device_mac}")

        if get_custom_platform() == "windows":
            # It needs to disable the services. Then, it can enable services and connect.
            self.bluetooth_disconnect(device_mac)

            Popen(["btcom", "-b", device_mac, "-c", "-s111e"]).wait()
            Popen(["btcom", "-b", device_mac, "-c", "-s110b"]).wait()

        else:
            Popen(["blueutil", "--wait-connect", str(device_mac), "60"]).wait()

    def bluetooth_disconnect(self, device_mac: str) -> None:
        """
        Method to do bluetooth disconnection
        :param device_mac: bt address of device
        :return none
        """
        Report.logInfo(f"Disconnect {device_mac}")

        if get_custom_platform() == "windows":
            # It needs to disable the services. Then, bluetooth will show disconnected.
            # btcom : Enables or disables remote bluetooth services, manipulates bluetooth COM ports.
            # -b : Bluetooth address of remote device in (XX:XX:XX:XX:XX:XX) format.
            # -r : Remove association between COM port and a remote service
            # -s : Remote service to use (Default is Serial Port Service)
            # Here, once the BT services (111e and 110b) are enabled, it will show connected on Windows settings.
            Popen(["btcom", "-b", device_mac, "-r", "-s111e"]).wait()
            Popen(["btcom", "-b", device_mac, "-r", "-s110b"]).wait()

        else:
            Popen(["blueutil", "--disconnect", str(device_mac)]).wait()

    def bluetooth_discover_services(self, device_mac=None) -> None:
        """
        Method to discover nearby devices' bluetooth service
        :param device_mac: bt address of device
        :return none
        """
        Report.logInfo("Run bluetooth discovery")

        if get_custom_platform() == "windows":
            # -s  Make service discovery. Optionally set output format for the list of services.
            # %sn% : service name. %su% : UUID.
            Popen(["btdiscovery", "-b", device_mac, "-s%sn%%su%"]).wait()

        else:
            Popen(["blueutil", "--inquiry"]).wait()

    def bluetooth_pair(self, device_mac: str, device_name: str) -> (bool, bool):
        """
        Method to do bluetooth pairing
        :param device_mac: bt address of device
        :param device_name: name of device
        :return bool : True for success, False for fail
        """
        pair_success = True
        bt_search_result = True

        Report.logInfo(f"Pair {device_name} {device_mac}")

        if get_custom_platform() == "windows":

            #unpiar all devcie, make sure all unwnated devcie be unparied before testing
            Popen(["btpair", "-u"]).wait()

            # Kill Settings process if exist
            for proc in psutil.process_iter():
                if proc.name() == "SystemSettings.exe":
                    proc.kill()
                    Report.logInfo(f'Process {proc.name()} is killed.')

            # Launch Windows Settings - Bluetooth
            Report.logInfo("Launch Windows Settings - Bluetooth")
            Popen(["start", "ms-settings:bluetooth"], shell=True).wait()
            time.sleep(2)

            # Attach driver to Settings - Bluetooth
            driver = global_variables.driver
            app = GetDriverForOpenApp()
            Report.logInfo("Get driver of Settings")
            driverRaw = app.getDriver("Settings")
            self.driver = EventFiringWebDriver(driverRaw, CustomListener())
            global_variables.driver = self.driver

            # Add Bluetooth device
            self.look_element(WinAppLocators.ADD_BLUETOOTH_OR_OTHER_DEVICE).click()
            self.look_element(WinAppLocators.BLUETOOTH).click()
            element = (By.XPATH, f"//*[@Name='{device_name}']")
            # Click vertical large increase to scroll down if it doesn't show element on the window
            count = 0
            try:
                while not self.verify_element(element, timeunit=5):
                    if (count == 0) or ((count % 2) != 0):  # Scroll down
                        if self.verify_element(WinAppLocators.VERTICAL_LARGE_INCREASE, timeunit=1):
                            self.look_element(WinAppLocators.VERTICAL_LARGE_INCREASE, scroll_flag=False, skip_exception=True).click()
                    elif (count % 2) == 0:  # Scroll to top every 2 times
                        if self.verify_element(WinAppLocators.VERTICAL_LARGE_DECREASE, timeunit=1):
                            self.look_element(WinAppLocators.VERTICAL_LARGE_DECREASE, scroll_flag=False, skip_exception=True).click()

                    # If count is bigger than 10, report failed and break the loop
                    if count >= 10:
                        bt_search_result = False
                        Report.logInfo("Fail to search the expected device")
                        break
                    count += 1

                if bt_search_result and (count < 10):
                    try:
                        self.look_element(
                            element=(By.XPATH, f"//Text[@Name='{device_name}' and @AutomationId='TextDeviceName']"),
                            skip_exception=True, timeout=60).click()
                        self.look_element(WinAppLocators.DONE, skip_exception=True).click()
                        time.sleep(3)
                    except:
                        pair_success = False
                        Report.logInfo("Fail to pair with the expected device")
            except:
                #exception during BT discovery
                pair_success = False
                bt_search_result = False
                Report.logInfo("Exception during BT discovery or pairing")



            # Return driver control back
            global_variables.driver.close()
            global_variables.driver = driver

            #############Second solution###########################
            # # -p0000 : Pair your computer with remote device using specified PIN code.
            # # 	       PIN code is optional (since version 1.2.0.56). If not provided "0000" is used.
            # Popen(["btpair", "-n", device_name, "-p0000"]).wait()
            # self.run_sikuli_win_bt_pair()
            #######################################################

        else:
            self.bluetooth_unpair(device_mac=device_mac, device_name=device_name)
            count = 1
            output_text = ""
            shcmd = "ls -l /dev/tty.*"
            target = "/dev/tty." + device_name.replace(" ", "")
            while target not in output_text:
                if count <= 3:
                    Report.logInfo(f"Pairing Try: {count}")
                    shcmd_mac_ver = "sw_vers"
                    output_bytes = check_output([shcmd_mac_ver], shell=True)
                    output_text = output_bytes.decode("utf-8")
                    macos_version = re.findall(r"\d+\.\d+", output_text)
                    Report.logInfo(f"MacOS version is: {macos_version}")
                    #  macOS version newer than 13, it's new UI, using pair_new_device_bt_macos_after_13.scpt
                    if float(macos_version[0]) >= 13:
                        Popen(["osascript", "pair_new_device_bt_macos_after_13.scpt", str(device_name), str(DIR_PATH)], cwd=DIR_PATH).wait()
                    #  If macOS version is 12, it's old UI, using pair_new_device_bt_macos_12.scpt
                    else:
                        Popen(["osascript", "pair_new_device_bt_macos_12.scpt", str(device_name)], cwd=DIR_PATH).wait()
                    count += 1
                elif count > 3:
                    Report.logFail("Pairing FAILED.")
                    pair_success = False
                    bt_search_result = False
                    break
                output_bytes = check_output([shcmd], shell=True)
                output_text = output_bytes.decode("utf-8")
                if target in output_text:
                    pair_success = True
                    bt_search_result = True


            ####################Applescript#######################
            # on run argv
            # return connectDevice(item 1 of argv)
            # end run
            # on connectDevice(deviceName)
            # tell application "System Preferences"
            # reveal pane "com.apple.preferences.Bluetooth"
            #   activate
            # end tell
            # tell application "System Events" to tell process "System Preferences"
            #   with timeout of 40 seconds
            # 	    if (exists window "Bluetooth") exists then
            # 	    delay 10
            # 		click window "Bluetooth"
            # 		set elements to entire contents of table 1 of scroll area 1 of window "Bluetooth"
            # 	of application process "System Preferences" of application "System Events"
            # 		repeat with e in elements
            # 			if class of e is UI element and name of e is deviceName then
            # 				click button of e
            # 			end if
            # 		end repeat
            # 	end if
            # end timeout
            # end tell
            # delay 30
            # tell application "System Preferences"
            # 	close window "Bluetooth"
            # end tell
            # end connectDevice
            #############################################################

        return pair_success, bt_search_result
    #############Second solution###########################
    # def run_sikuli_win_bt_pair(self) -> None:
    #     """
    #     Method to run sikuli script, clicking Windows popup for bluetooth pairing
    #     :param none
    #     :return none
    #     """
    #     Report.logInfo("Running Sikuli script")
    #     filepath = str(UIBase.rootPath.parent) + "\Sikuli_Automation_System\scripts\windows_bluetooth_pair.sikuli"
    #     Popen(["java", "-jar", "C:\Sikuli\sikulixide-2.0.5.jar", "-r", filepath]).wait()
    #######################################################

    def bluetooth_unpair(self, device_mac: str, device_name: str) -> None:
        """
        Method to do bluetooth unpairing
        :param device_mac: bt address of device
        :param device_name: name of device
        :return none
        """
        Report.logInfo(f"Unpair {device_name} {device_mac}")

        if get_custom_platform() == "windows":

            # Kill Settings process if exist
            for proc in psutil.process_iter():
                if proc.name() == "SystemSettings.exe":
                    proc.kill()
                    Report.logInfo(f'Process {proc.name()} is killed.')

            # Launch Windows Settings - Bluetooth
            Report.logInfo("Launch Windows Settings - Bluetooth")
            Popen(["start", "ms-settings:bluetooth"], shell=True).wait()
            time.sleep(2)

            # Attach driver to Settings - Bluetooth
            driver = global_variables.driver
            app = GetDriverForOpenApp()
            Report.logInfo("Get driver of Settings")
            driverRaw = app.getDriver("Settings")
            self.driver = EventFiringWebDriver(driverRaw, CustomListener())
            global_variables.driver = self.driver

            # Remove device
            element = (
                By.XPATH,
                f"//ListItem[contains(@Name, '{device_name}')]//Button[contains(@AutomationId, 'DeviceOptionsButton')]")
            if get_current_system_version() == "11":  # Windows 11
                self.look_element(element).click()
                self.look_element(WinAppLocators.REMOVE_DEVICE).click()
            else:  # Windows 10
                element = (By.XPATH, f"//ListItem[contains(@Name, '{device_name}')]")
                self.look_element(element).click()
                self.look_element(WinAppLocators.REMOVE_DEVICE).click()
                self.press_enter_key()

            # Return driver control back
            global_variables.driver.close()
            global_variables.driver = driver

            #############Second solution for Windows##############
            #  Popen(["btpair", "-b", device_mac, "-u"]).wait() # Unpair specific MAC address via cmd line tool
            #  Popen(["btpair", "-u"]).wait() # Unpair all via cmd line tool
            #######################################################

        else:
            Popen(["blueutil", "--unpair", str(device_mac)]).wait()

    def bluetooth_power_ctrl(self, power_switch: bool) -> None:
        """
        Method to turn on/off PC's bluetooth
        :param power_switch: True for turning on, False for turning off
        :return none
        """
        if get_custom_platform() == "windows":
            asyncio.run(self.windows_bluetooth_power_ctrl(power_switch))

        else:
            if power_switch:
                power_switch = "1"
                Report.logInfo("PC bluetooth on")

            else:
                power_switch = "0"
                Report.logInfo("PC bluetooth off")
            Popen(["blueutil", "-p", power_switch]).wait()

    async def windows_bluetooth_power_ctrl(self, power_switch: bool) -> None:
        """
        Method to turn on/off Windows PC's bluetooth
        :param power_switch: True for turning on, False for turning off
        :return none
        """
        from winsdk.windows.devices import radios
        all_radios = await radios.Radio.get_radios_async()
        for this_radio in all_radios:
            if this_radio.kind == radios.RadioKind.BLUETOOTH:
                if power_switch:
                    result = await this_radio.set_state_async(radios.RadioState.ON)
                    Report.logInfo("PC bluetooth on")

                else:
                    result = await this_radio.set_state_async(radios.RadioState.OFF)
                    Report.logInfo("PC bluetooth off")
