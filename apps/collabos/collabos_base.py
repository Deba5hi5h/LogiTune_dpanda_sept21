import os
import sys
import time
from typing import Any, Callable

import requests
from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
import subprocess as sp

from apps.collabos import collabos_config
from apps.collabos.base_collabos_methods import CollabOsBaseMethods
from apps.collabos.coily.utilities import restart_adb_device_and_wait_for_boot, check_and_connect_device, \
    restart_adb_server
from apps.tune.helpers import get_python_version
from base import global_variables
from base.listener import CustomListener
from common.platform_helper import get_custom_platform
from extentreport.report import Report


class AppiumServiceCollabOS(AppiumService):

    def __init__(self, appium_port: str, device_ip: str, device_sn: str):
        super().__init__()
        self.appium_port = appium_port
        self.device_ip = device_ip
        self.device_sn = device_sn

    def start(self, **kwargs: Any) -> sp.Popen:
        Report.logInfo(f"Starting Appium service on PORT {self.appium_port}")
        return super().start(args=["--port", str(self.appium_port)], **kwargs)

    def restart_collabos_device_and_wait_for_boot(self):
        restart_adb_device_and_wait_for_boot(self.device_ip)

    def check_if_appium_server_is_already_running(self):
        try:
            res = requests.get(f"http://127.0.0.1:{self.appium_port}/status")
            if res.ok:
                res_json = res.json()
                if res_json.get('value').get('ready'):
                    return True
                return False
        except requests.exceptions.ConnectionError:
            return False

    @staticmethod
    def get_appium_server_details(self):
        try:
            res = requests.get(f"http://127.0.0.1:{self.appium_port}/status")
            if res.ok:
                return res.json()
        except requests.exceptions.ConnectionError:
            return False

    def check_appium_server_current_sessions(self):
        if global_variables.collabos_driver is None:
            return False
        try:
            res = (requests.get(
                f"http://127.0.0.1:{self.appium_port}/session/"
                f"{global_variables.collabos_driver.wrapped_driver.session_id}"))
            if res.ok:
                return True
            return False
        except (requests.exceptions.ConnectionError, Exception):
            return False

    @staticmethod
    def _close_appium_server_windows():
        os.system("taskkill /F /IM node.exe")

    @staticmethod
    def _close_appium_server_macos():
        os.system('killall node')

    def close_appium_server(self):
        if get_custom_platform() == "windows":
            self._close_appium_server_windows()
        else:
            self._close_appium_server_macos()
        time.sleep(5)


class CollabOsBase(CollabOsBaseMethods):

    @staticmethod
    def connect_to_collabos_app(port: str = "4723", device_sn: str = "",
                                device_ip: str = "") -> EventFiringWebDriver:
        """
        Args:
            port: The port number to connect to the Appium server. Defaults to "4723".
            device_sn: The serial number of the device to connect to. Defaults to an empty string.
            device_ip: The IP address of the device to connect to. Defaults to an empty string.

        Returns:
            An instance of EventFiringWebDriver connected to the CollabOS Android application.

        Raises:
            Exception: If there is an error while connecting to the CollabOS app.

        """
        desired_capabilities = {
            'platformName': 'Android',
            'deviceName': device_sn,
            'platformVersion': '10.0',
            'udid': f"{device_ip}:5555",
            'acceptInsecureCerts': True,
            'newCommandTimeout': 0,
            'noReset': True,
            'ignoreHiddenApiPolicyError': True
        }

        Report.logInfo("Launching to CollabOS android application.")
        try:
            if get_python_version() < 312:
                driver_raw = webdriver.Remote(f'http://localhost:{port}/wd/hub',
                                              desired_capabilities)
            else:
                from appium.options.common import AppiumOptions
                desired_capabilities['automationName'] = 'UiAutomator2'
                options = AppiumOptions()
                options.load_capabilities(desired_capabilities)
                driver_raw = webdriver.Remote(f'http://localhost:{port}',
                                              options=options)
            driver_raw.implicitly_wait(collabos_config.implicit_wait)
            driver = EventFiringWebDriver(driver_raw, CustomListener())
            global_variables.collabos_driver = driver
            return global_variables.collabos_driver
        except Exception as e:
            Report.logException(f'Error while connecting to CollabOS app - {repr(e)}')
            raise e


class CollabOsOpenApp:

    def __init__(self, appium_service: AppiumServiceCollabOS, connect_process: Callable,
                 force: bool):
        self.appium_service = appium_service
        self.connect_process = connect_process
        self.force = force

    def connect_to_android_app(self, retry: int = 0) -> None:
        if retry == 5:
            Report.logException("Could not connect to Appium with 5 retries")
            return
        try:
            if not self.appium_service.check_if_appium_server_is_already_running():
                self.appium_service.start()
            if not self.appium_service.check_appium_server_current_sessions():
                try:
                    global_variables.collabos_driver.wrapped_driver.quit()
                except (InvalidSessionIdException, AttributeError):
                    Report.logInfo("Forced Open App: A session not quited because it does not exist anymore")
                global_variables.collabos_driver = self.connect_process()
            if not self.appium_service.check_appium_server_current_sessions() and retry < 5:
                Report.logInfo("failed session - retrying")
                retry += 1
                self.connect_to_android_app(retry=retry)
        except Exception as ex:
            if "An unknown server-side error occurred while processing the command" in ex.msg:
                Report.logInfo(ex.msg)
                self.appium_service.close_appium_server()
                if retry < 4:
                    retry += 1
                    Report.logInfo(f'Reconnecting {retry} time...')
                    try:
                        global_variables.collabos_driver = None
                        if self.appium_service:
                            self.appium_service.stop()
                        restart_adb_server()
                        self.appium_service.start()
                        check_and_connect_device(self.appium_service.device_ip)
                        self.connect_to_android_app(retry)
                        Report.logInfo(f'Driver connected successfully to Coily')
                    except Exception as e:
                        Report.logInfo(f'{retry} retry - {repr(e)}')
