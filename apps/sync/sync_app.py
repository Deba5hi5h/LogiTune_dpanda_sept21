import json
import os
import shutil
import time
import subprocess
from typing import Optional

import psutil
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import requests
from webdriver_manager.core.driver_cache import DriverCacheManager

from apps.sync import sync_config
from base import base_settings, global_variables
from base.base_ui import UIBase
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from base.listener import CustomListener
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from locators.win_ui_locators import SyncAppLocators

CHROME_DRIVER_DIR = os.path.join(str(UIBase.rootPath), "drivers", "chromedriver_sync")
CHROME_DRIVER_JSON = os.path.join(CHROME_DRIVER_DIR, ".wdm", "drivers.json")


class SyncApp(UIBase):

    def __init__(self):
        self.options = Options()
        root_path = str(UIBase.rootPath)
        if get_custom_platform() == "windows":
            self.options.binary_location = sync_config.SYNC_APP_PATH_WIN
            self.chrome_path = f"{root_path}/drivers/chromedriver_win_sync.exe"
        else:
            self.options.binary_location = sync_config.SYNC_APP_PATH_MAC
            self.chrome_path = f"{root_path}/drivers/chromedriver_mac_sync"

    def open_sync_app(self, fre=False):
        """
        Method to open Sync App on Windows/Mac. Relaunch App if it crashes on Mac

        :param fre:
        :return :
        """
        Report.logInfo("Launching Sync App")
        self.launch_sync_app(fre=fre)
        UIBase.highlight_flag = False
        if not fre and not self.verify_element(SyncAppLocators.ROOM_LINK, timeunit=60):
            global_variables.driver.quit()
            if get_custom_platform() == 'macos':
                os.system('pkill LogiSyncHandler')
                os.system('pkill LogiSyncMiddleware')
                os.system('pkill LogiSyncProxy')
                time.sleep(10)
            Report.logWarning("Re Launching Sync App after restarting service due to crash")
            self.launch_sync_app()
        return global_variables.driver

    def launch_sync_app(self, fre=False):
        """
        Method to launch Sync App and complete start up wizard if exists
        This is used by openSyncApp

        :param fre:
        :return :
        """

        Report.logInfo("Prepare chromedriver file.")
        if not os.path.isfile(CHROME_DRIVER_JSON):
            Report.logInfo("No chromedriver files available. Install newest "
                           "chromedriver from server.")
            self._chrome_driver_manager(path=CHROME_DRIVER_DIR)
            print(CHROME_DRIVER_DIR)
            assert os.path.isfile(
                CHROME_DRIVER_JSON
            ), f"Chromedriver downloaded incorrectly. Missing {CHROME_DRIVER_JSON}"

        chrome_driver = self._get_chrome_driver_version_from_json()

        if not os.path.isfile(chrome_driver):
            Report.logInfo("Chromedriver file is not available. Remove whole "
                           "folder and download chromedriver again.")
            self.close_chromedriver()
            shutil.rmtree(CHROME_DRIVER_DIR)
            time.sleep(1)
            self._chrome_driver_manager(path=CHROME_DRIVER_DIR)
            assert os.path.isfile(
                CHROME_DRIVER_JSON
            ), f"Chromedriver downloaded incorrectly. Missing {CHROME_DRIVER_JSON}"
            chrome_driver = self._get_chrome_driver_version_from_json()
            time.sleep(10)
        try:
            driverRaw = webdriver.Chrome(
                executable_path=chrome_driver,
                desired_capabilities=DesiredCapabilities.CHROME,
                options=self.options)
        except WebDriverException as ex:
            Report.logInfo(
                "Downloaded chrome driver does not support current Sync app.")
            Report.logInfo(ex.msg)
            if "This version of ChromeDriver only supports" in ex.msg:
                self.close_chromedriver()
                shutil.rmtree(CHROME_DRIVER_DIR)
                time.sleep(1)

                if not os.path.isdir(CHROME_DRIVER_DIR):
                    version = self._extract_driver_version_from_message(ex)
                    Report.logInfo("Extracted version from the exception: " + version)
                    if version.startswith("114"):
                        official_driver_version_response = \
                            self._get_official_chromedriver_release_from_server(version)

                        Report.logInfo(
                            f"Downloaded chrome driver ver: {official_driver_version_response}"
                        )
                        self._chrome_driver_manager(version=official_driver_version_response, path=CHROME_DRIVER_DIR)
                        assert os.path.isfile(
                            CHROME_DRIVER_JSON), f"Chromedriver downloaded " \
                                                 f"incorrectly. Missing {CHROME_DRIVER_JSON}"
                        chrome_driver = self._get_chrome_driver_version_from_json()
                        driverRaw = webdriver.Chrome(
                            executable_path=chrome_driver,
                            desired_capabilities=DesiredCapabilities.CHROME,
                            options=self.options)
                    else:
                        self._chrome_driver_manager(path=CHROME_DRIVER_DIR, version=version)
                        assert os.path.isfile(
                            CHROME_DRIVER_JSON
                        ), f"Chromedriver downloaded incorrectly. Missing {CHROME_DRIVER_JSON}"
                        chrome_driver = self._get_chrome_driver_version_from_json()
                        driverRaw = webdriver.Chrome(
                            executable_path=chrome_driver,
                            desired_capabilities=DesiredCapabilities.CHROME,
                            options=self.options)

        sync_config.base_driver = driverRaw
        self.driver = EventFiringWebDriver(driverRaw, CustomListener())
        self.driver.implicitly_wait(base_settings.IMPLICIT_WAIT)
        global_variables.driver = self.driver
        if fre:
            return
        UIBase.highlight_flag = False
        if self.verify_element(SyncAppLocators.ROOM_LINK, wait_for_visibility=True):
            self.look_element(SyncAppLocators.ROOM_LINK)
        elif self.verify_element(SyncAppLocators.GET_STARTED, 30):
            self.look_element(SyncAppLocators.GET_STARTED).click()
            if self.verify_element(SyncAppLocators.EMAIL_SETUP, timeunit=5):
                self.look_element(SyncAppLocators.EMAIL_SETUP).click()
            self.look_element(SyncAppLocators.SKIP_SETUP).click()
        self.wait = WebDriverWait(global_variables.driver, base_settings.EXPLICIT_WAIT)

    @staticmethod
    def _get_chrome_driver_version_from_json() -> str:
        """ Method to get a path to chromedriver from drivers.json

        @return: path to chromedriver
        """
        with open(CHROME_DRIVER_JSON) as file:
            tmp = json.load(file)

        try:
            bin_path_tmp = next(iter(tmp.values()))
            chrome_driver_path = bin_path_tmp['binary_path']
            print(chrome_driver_path)
            return chrome_driver_path
        except KeyError as e:
            Report.logException(f"Missing: {e}")

    @staticmethod
    def _extract_driver_version_from_message(exception_message: str) -> str:
        """ Method to convert chromedriver version from exception message to
        version accepted by chrome server API, i.e. 98.0.4758

        @param exception_message: exception message from WebDriverException
        @return: chrome driver version
        """
        list_msg = exception_message.msg.split('\n')
        # whole_driver_ver = list_msg[-1].split("Current browser version is ", 1)[1]
        try:
            whole_driver_ver = list_msg[-1].split("Current browser version is ", 1)[1]
        except:
            return "87"
        splitted_driver_ver = whole_driver_ver.split(".")
        return '.'.join(splitted_driver_ver[0:-2])

    @staticmethod
    def _get_official_chromedriver_release_from_server(driver_version: str) -> str:
        """ Method to query chrome server for official version for chromedriver

        @param driver_version:
        @return: official chromedriver version from chrome server
        """
        result = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{driver_version}")
        return result.text

    def close_sync_app(self):
        """
        Method to close Sync App opened through script

        :param :
        :return :
        """
        global_variables.driver.quit()

    @staticmethod
    def restart_sync_services():
        """
        Method to restart Sync Services - LogiSyncHandler, LogiSyncMiddleware, LogiSyncProxy

        :param none
        :return none
        """
        if get_custom_platform() == 'macos':
            os.system('pkill LogiSyncHandler')
            os.system('pkill LogiSyncMiddleware')
            os.system('pkill LogiSyncProxy')
        else:
            time.sleep(2)
            p = subprocess.run([str(UIBase.rootPath) + "\\WinApp\\restart_sync_services.bat"], capture_output=True)
            time.sleep(3)  # Wait for file to be created
            while True:
                flag = False
                file1 = open(str(UIBase.rootPath) + "\\WinApp\\tmp_read.txt", "r")
                for line in file1:
                    # check finish is present in line or not
                    if "finish" in line:
                        flag = True
                if flag:
                    break
                file1.close()

    @staticmethod
    def close_chromedriver():
        if get_custom_platform() == 'macos':
            os.system('pkill -9 chromedriver')
        else:
            for proc in psutil.process_iter():
                if 'chromedriver.exe' in proc.name():
                    os.system("taskkill /f /IM chromedriver.exe")

    @staticmethod
    def _chrome_driver_manager(path: str = CHROME_DRIVER_DIR, version: Optional[str] = None
                               ) -> None:
        Report.logInfo("Downloading chrome driver using WDM")
        ChromeDriverManager(
            driver_version=version, cache_manager=DriverCacheManager(root_dir=path)).install()
