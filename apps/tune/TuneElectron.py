import getpass
import json
import os
import shutil
import subprocess
import re
import unittest
import sys

import requests
from typing import Optional, Dict, Tuple, List

import psutil
import selenium.common.exceptions
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from apps.tune.helpers import get_python_version, return_valid_windows_logi_tune_path
from apps.tune.TuneAppSettings import TuneAppSettings
from apps.collabos.coily.tune_coily_config import NEVER_BLOCK_PERIPHERALS
from base.base_ui import UIBase
from base.listener import CustomListener
from common.decorators import Singleton
from common.platform_helper import get_custom_platform, verify_file_existence
from common.comparators import Comparator
from common.usb_switch import *
from common.logs_storer import store_failed_testcase_logs_on_server
from datetime import datetime
from locators.tunes_ui_locators import *
from base.global_variables import ROOT_DIRECTORY, TUNE_DEBUG_PORT
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.usb_hid_communication_base import \
    UsbHidCommunicationBase

TUNE_FEATURES_FILENAME = 'tune-features.cfg'
LOCAL_UPDATE_ENABLED_STRING = "local_update_enabled=true"
DIR_UTILS_PATH = os.path.join(ROOT_DIRECTORY, "firmware_tunes", "utils")

CHROME_DRIVER_DIR = os.path.join(str(UIBase.rootPath),
                                 "drivers",
                                 "chromedriver_tune")
CHROME_DRIVER_JSON = os.path.join(CHROME_DRIVER_DIR, ".wdm", "drivers.json")

STRICT_CHECK_DEVICES = ['Brio', 'Zone Wireless', 'Zone Wired', "Zone Vibe 125"]


class EventFiringWebDriverWrapper(EventFiringWebDriver):
    instance = None

    def __new__(cls, driver, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

@Singleton
class TuneElectron(UIBase):
    driver = None

    def open_tune_app(self, modify_json=False,
                      clean_logs=False,
                      tune_env: Optional[str] = None,
                      update=False, retry=0):
        Report.logInfo("Prepare LogiTune application before opening.")
        UIBase.logi_tune_flag = True

        if get_custom_platform() == "windows":
            os_logitune_close = self.close_tune_app_windows
            os_logitune_open_path = f"{str(UIBase.rootPath)}/WinApp/tune.bat {TUNE_DEBUG_PORT}"
        else:
            os_logitune_close = self.close_tune_app_macos
            os_logitune_open_path = f"sh {str(UIBase.rootPath)}/WinApp/tune.sh {TUNE_DEBUG_PORT}"

        os_logitune_close()
        time.sleep(5)
        if modify_json:
            tune_settings = TuneAppSettings()
            tune_settings.adjust_logitune_settings_file(tune_env=tune_env)
            time.sleep(5)
        if clean_logs:
            self.clean_logitune_folder_logs()
        os.system(os_logitune_open_path)

        Report.logInfo("Prepare chromedriver file.")
        if not os.path.isfile(CHROME_DRIVER_JSON):
            Report.logInfo("No chromedriver files available. Install newest "
                           "chromedriver from server.")
            self._chrome_driver_manager(path=CHROME_DRIVER_DIR)
            assert os.path.isfile(
                CHROME_DRIVER_JSON
            ), f"Chromedriver downloaded incorrectly. Missing {CHROME_DRIVER_JSON}"

        chrome_driver = self._get_chrome_driver_version_from_json()

        if not os.path.isfile(chrome_driver):
            Report.logInfo("Chromedriver file is not available. Remove whole "
                           "folder and download chromedriver again.")
            shutil.rmtree(CHROME_DRIVER_DIR)
            time.sleep(1)
            self._chrome_driver_manager(path=CHROME_DRIVER_DIR)
            assert os.path.isfile(
                CHROME_DRIVER_JSON
            ), f"Chromedriver downloaded incorrectly. Missing {CHROME_DRIVER_JSON}"
            chrome_driver = self._get_chrome_driver_version_from_json()

        time.sleep(10)

        Report.logInfo("Launching LogiTune App")
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress",
                                               "127.0.0.1:9222")

        try:
            if get_python_version() < 312:
                driverRaw = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            else:
                from selenium.webdriver import ChromeService
                service = ChromeService(executable_path=chrome_driver)
                driverRaw = webdriver.Chrome(service=service, options=chrome_options)

        except WebDriverException as ex:
            Report.logInfo(ex.msg)
            driverRaw = None
            if "This version of ChromeDriver only supports" in ex.msg:
                Report.logInfo(
                    "Downloaded chrome driver does not support current LogiTune.")
                shutil.rmtree(CHROME_DRIVER_DIR)
                time.sleep(1)

                if not os.path.isdir(CHROME_DRIVER_DIR):
                    version = self._extract_driver_version_from_message(ex.msg)
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

                    if get_python_version() < 312:
                        driverRaw = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
                    else:
                        from selenium.webdriver import ChromeService
                        service = ChromeService(executable_path=chrome_driver)
                        driverRaw = webdriver.Chrome(service=service, options=chrome_options)
            else:
                Report.logInfo('Selenium unable to connect to Logi Tune')
                if retry < 3:
                    retry += 1
                    Report.logInfo(f'Reconnecting {retry} time...')
                    try:
                        driverRaw = self.open_tune_app(modify_json, clean_logs,
                                                       tune_env, update, retry).wrapped_driver
                        Report.logInfo(f'Driver connected successfully to Logi Tune!')
                    except WebDriverException as e:
                        Report.logInfo(f'{retry} retry - {repr(e)}')

        self.driver = EventFiringWebDriverWrapper(driverRaw, CustomListener())
        handles = self.driver.window_handles
        for handle in handles:
            self.driver.switch_to.window(handle)
            global_variables.driver = self.driver
            UIBase.highlight_flag = False
            if self.verify_element(TunesAppLocators.UPDATE_APP_NOW, timeunit=2):
                if not update:
                    Report.logInfo('Clicking "Remind me later" button for Logi Tune update available')
                    self.look_element(TunesAppLocators.UPDATE_APP_LATER_BUTTON).click()
                break
            elif self.verify_element(TunesAppLocators.SETTINGS_MENU, timeunit=2):
                break
            elif self.verify_element(TunesAppLocators.TUNE_UPDATED_OK_BUTTON, timeunit=2):
                Report.logInfo('Clicking "OK" button for Logi Tune update successful prompt')
                self.look_element(TunesAppLocators.TUNE_UPDATED_OK_BUTTON).click()
                break

        if not self.verify_element(TunesAppLocators.SETTINGS_MENU, timeunit=2):
            return self.open_tune_app(modify_json, clean_logs, tune_env, update, retry)

        self.wait = WebDriverWait(global_variables.driver, 5)
        return self.driver

    @staticmethod
    def _chrome_driver_manager(path: str = CHROME_DRIVER_DIR, version: Optional[str] = None
                               ) -> None:
        ChromeDriverManager(
            driver_version=version, cache_manager=DriverCacheManager(root_dir=path)).install()

    @staticmethod
    def _extract_driver_version_from_message(exception_message: str) -> str:
        """ Method to convert chromedriver version from exception message to
        version accepted by chrome server API, i.e. 98.0.4758

        @param exception_message: exception message from WebDriverException
        @return: chrome driver version
        """
        list_msg = exception_message.split('\n')
        whole_driver_ver = list_msg[-1].split("Current browser version is ", 1)[1]
        splitted_driver_ver = whole_driver_ver.split(".")
        return '.'.join(splitted_driver_ver[0:-1])

    @staticmethod
    def _get_official_chromedriver_release_from_server(driver_version: str) -> str:
        """ Method to query chrome server for official version for chromedriver

        @param driver_version:
        @return: official chromedriver version from chrome server
        """
        result = requests.get(
            f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{driver_version}"
        )
        if 'The specified key does not exist' in result.text:
            result = requests.get(
                'https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone.json'
            )
            result_json = result.json()
            latest_versions = result_json.get('milestones')
            for version, value in latest_versions.items():
                if version == driver_version.split('.')[0]:
                    return value.get('version')
        return result.text

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
            return chrome_driver_path
        except KeyError as e:
            Report.logException(f"Missing: {e}")

    def navigate_to_main_screen(self, device_name: Optional[str] = None):
        if device_name in ["Zone Wireless 2", "Zone 950"]:
            # temporary solution for Cybermorph
            if self.verify_back_button_cybermorph():
                self.click_back_button_cybermorph()

        if self.verify_back_button_to_device_settings():
            self.click_back_button_to_device_settings()
        if self.verify_back_button_to_my_devices():
            self.click_back_button_to_my_devices()
        if self.verify_home():
            self.click_home()
        else:
            raise Exception("No Home Page Found")

    def connect_tune_app(self, device_name: Optional[str] = None):
        try:
            self.driver.window_handles
            self.navigate_to_main_screen()
            return self.driver
        except Exception as e:
            self.open_tune_app(clean_logs=True)

    @staticmethod
    def close_tune_app_macos():
        os.system('pkill -9 LogiTune')
        os.system('pkill -9 LogiTune')  # needed to kill Logi_Calendar

    @staticmethod
    def close_tune_app_windows():
        for proc in psutil.process_iter():
            try:
                if 'LogiTune.exe' in proc.name():
                    os.system("taskkill /IM LogiTune.exe /F")
                if 'LogiTuneAgent.exe' in proc.name():
                    os.system("taskkill /IM LogiTuneAgent.exe /F")
                if 'chromedriver.exe' in proc.name():
                    os.system("taskkill /IM chromedriver.exe /F")
            except psutil.NoSuchProcess:
                continue

    def scroll_into_view(self, element: WebElement, scroll_area_locator: Tuple[str, str]) -> None:
        scroll_area = self.look_element(scroll_area_locator, scroll_flag=False)
        self.driver.execute_script("arguments[0].scrollTo(0, 0);", scroll_area)
        self.driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", scroll_area,
                                   element.rect['y'] - scroll_area.rect['y'] - element.rect['height'])

    def close_tune_app(self):
        Report.logInfo("Close LogiTune application.")
        if get_custom_platform() == "windows":
            self.close_tune_app_windows()
        else:
            self.close_tune_app_macos()
        self.driver = None
        time.sleep(5)

    def clean_logitune_folder_logs(self):
        Report.logInfo("Clear folders with application logs.")
        folders = []
        if get_custom_platform() == "windows":
            folders = [
                r'C:\ProgramData\Logitech\Tune\UI',
                f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\logitune\\LogiTuneLogs\\LogiTuneBackEndLogs",
                f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\logitune\\CrashDumps"
            ]
        if get_custom_platform() == "macos":
            folders = [
                '/Users/Shared/logitune/UI',
                f"/Users/{getpass.getuser()}/Library/Application Support/logitune/LogiTuneAgentLogs",
                f"/Users/{getpass.getuser()}/Library/Application Support/logitune/LogiTuneUpdaterLogs"
            ]

        for folder in folders:
            self.__delete_logs(folder)

    def get_window_position_and_size(self) -> dict:
        return {
            "x": self.driver.execute_script("return window.screenX"),
            "y": self.driver.execute_script("return window.screenY"),
            "w": self.driver.execute_script("return window.outerWidth"),
            "h": self.driver.execute_script("return window.outerHeight"),
        }

    def save_logitune_logs_in_testlogs(self, testlogs_path, test_name) -> None:
        Report.logInfo("Export Logi Tune application logs.")
        try:
            logs_path = self.__export_logitune_logs()
            logs_destination_path = os.path.join(
                testlogs_path, f"LOGITUNE_LOGS_{test_name}.zip")
            shutil.move(logs_path, logs_destination_path)
            logs_server_link = store_failed_testcase_logs_on_server(logs_path=logs_destination_path)
            if logs_server_link:
                Report.logInfo(f"<a href={logs_server_link}>Download Logs</a>", color="yellow")
            else:
                Report.logInfo("Logging Server not responded, update logs failed", color='yellow')
        except Exception as e:
            Report.logInfo(f'Problem with saving test logs: {str(e)}', color='yellow')

    @staticmethod
    def __export_logitune_logs():
        try:
            if get_custom_platform() == "windows":
                cmd = os.path.join(return_valid_windows_logi_tune_path(), 'logitune-diagnostic-report.cmd')
                res = subprocess.check_output(f'"{cmd}"',
                                              shell=True,
                                              stdin=subprocess.PIPE)
                formatted_res = res.decode('utf-8').split('\n')
                for line in formatted_res:
                    message = f'A zip file "C:\\Users\\{os.getlogin()}\\Logitune-report.zip" generated. Send it to developers.'
                    if message in line:
                        return f"C:\\Users\\{os.getlogin()}\\Logitune-report.zip"
            if get_custom_platform() == "macos":
                cmd = r'/Library/Application\ Support/logitune/logitune-diagnostic-report.sh'
                res = subprocess.check_output(cmd, shell=True)
                formatted_res = res.decode('utf-8').split('\n')
                for line in formatted_res:
                    if "Finished. Please send this file to support: " in line:
                        return line.split(': ')[1]
        except Exception as e:
            Report.logException(str(e))

    @staticmethod
    def __delete_logs(directory: str) -> None:
        if not os.path.isdir(directory):
            return
        for filename in os.listdir(directory):
            try:
                os.remove(os.path.join(directory, filename))
                print(f'File {filename} was deleted!')
            except Exception as e:
                print(f'Cannot delete {filename}, exception - {e}')

    def verify_image_size(self, locator: Tuple[str, str]) -> bool:
        """ Method to verify if image is dispalyed.
            The function checks wether exist image's dimentions.

        @return: True if image has non-zero dimentions, False otherwise
        """
        element = self.look_element(locator)

        if element.size['width'] > 0 and element.size['height'] > 0:
            return True

        return False

    def verify_tune_processes_are_active(self):
        time.sleep(2)
        if get_custom_platform() == "windows":
            tune_app_name = "LogiTune.exe"
        else:
            tune_app_name = "LogiTune"

        proc_list = []
        for proc in psutil.process_iter():
            proc_list.append(proc.name())
        if tune_app_name not in proc_list:
            Report.logPass('LogiTune is successfully closed')
        else:
            Report.logFail('LogiTune is not closed.')

    def verify_tune_is_running(self):
        if get_custom_platform() == "windows":
            tune_app_name = "LogiTune.exe"
        else:
            tune_app_name = "LogiTune"

        proc_list = []
        for proc in psutil.process_iter():
            proc_list.append(proc.name())
        if tune_app_name in proc_list:
            Report.logPass('LogiTune is running.')
        else:
            Report.logFail('LogiTune is not running')

    def reopen_tune_app(self):
        self.close_tune_app()
        self.open_tune_app()
        self.driver.implicitly_wait(0)

    def relaunch_tune_app(self, open_my_devices_tab: Optional[bool] = True):
        self.close_tune_app()
        self.open_tune_app()
        if self.verify_home():
            if open_my_devices_tab:
                self.open_my_devices_tab()

    def verify_back_button_cybermorph(self):
        return self.verify_element(TunesAppLocators.BACK_CYBERMORPH, timeunit=2)

    def verify_back_button_to_my_devices(self):
        return self.verify_element(TunesAppLocators.BACK_TO_MY_DEVICES, timeunit=2)

    def verify_back_button_to_device_settings(self):
        return self.verify_element(TunesAppLocators.BACK_TO_DEVICE_SETTINGS, timeunit=2)

    def verify_back_to_device(self):
        return self.verify_element(TunesAppLocators.DEVICE_BACK, timeunit=2)

    def verify_button_functions_back(self):
        return self.verify_element(TunesAppLocators.DEVICE_BUTTON_FUNCTIONS_BACK, timeunit=2)

    def verify_no_devices_connected(self):
        return self.verify_element(TunesAppLocators.NO_DEVICE_CONNECTED)

    def verify_headsets_header(self):
        return self.verify_element(TunesAppLocators.HEADSETS_HEADER)

    def verify_webcams_header(self):
        return self.verify_element(TunesAppLocators.WEBCAMS_HEADER)

    def verify_docks_header(self):
        return self.verify_element(TunesAppLocators.DOCKS_HEADER)

    def verify_streaming_light_header(self):
        return self.verify_element(TunesAppLocators.STREAMING_LIGHT_HEADER)

    def verify_mice_header(self):
        return self.verify_element(TunesAppLocators.MICE_HEADER)

    def verify_keyboards_header(self):
        return self.verify_element(TunesAppLocators.KEYBOARDS_HEADER)

    def verify_supported_device_label(self, timeout: Optional[int] = None):
        if timeout:
            self.verify_element(TunesAppLocators.SUPPORTED_DEVICES_LINK, timeunit=timeout)
        else:
            self.verify_element(TunesAppLocators.SUPPORTED_DEVICES_LINK)

    def verify_device_displayed_on_supported_list(self, device_name):
        return self.verify_element(TunesAppLocators.SUPPORTED_DEVICE,
                                   param=device_name)

    def verify_device_name_displayed(self, device_name, exact_name: bool = False) -> bool:
        if device_name in ["Brio", "Zone Wireless"] or exact_name:
            return self.verify_element(TunesAppLocators.SUPPORTED_DEVICE_VER1,
                                       param=device_name)
        return self.verify_element(TunesAppLocators.SUPPORTED_DEVICE,
                                   param=device_name)

    def verify_device_connected(self) -> bool:
        """ Method to verify if CONNECTED label is dispalyed for device.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element_by_text(TunesAppLocators.DEVICE_CONNECTED, expected_text="CONNECTED")

    def verify_device_image(self) -> bool:
        """ Method to verify if device image is dispalyed for device.
            The function does not distinguish devices (or any other graphic) yet.

        @return: True if label is displayed, False otherwise
        """
        if self.verify_element(TunesAppLocators.DEVICE_IMAGE):
            if self.verify_image_size(TunesAppLocators.DEVICE_IMAGE):
                return True

        return False

    def verify_go_back_home_button(self) -> bool:
        """ Method to verify if go back home button is dispalyed for device.

        @return: True if label is displayed, False otherwise
        """
        if self.verify_element((TunesAppLocators.GO_BACK_HOME)):
            if self.verify_image_size(TunesAppLocators.GO_BACK_HOME):
                return True

        return False

    def verify_device_info_button(self) -> bool:
        """ Method to verify if device info button is dispalyed for device.

        @return: True if label is displayed, False otherwise
        """
        if self.verify_element(TunesAppLocators.INFO_BUTTON):
            if self.verify_image_size(TunesAppLocators.INFO_BUTTON):
                return True

        return False

    def verify_headset_connected(self) -> bool:
        """ Method to verify if CONNECTED label is dispalyed for the headset.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element_by_text(TunesAppLocators.DEVICE_CONNECTED, expected_text="CONNECTED")

    def verify_sidetone_displayed(self) -> bool:
        """ Method to verify if Sidetone label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.SIDETONE_LABEL)

    def verify_mic_level_displayed(self) -> bool:
        """ Method to verify is Mic level label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.MIC_LEVEL_LABEL)

    def verify_equalizer_displayed(self) -> bool:
        """ Method to verify is Equalizer label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.EQUALIZER)

    def verify_headset_diagnostics_displayed(self) -> bool:
        """ Method to verify both Diagnostics label and Diagnostics button are displayed.

        @return: True if both label and button are displayed, False otherwise
        """
        result1 = self.verify_element(TunesAppLocators.HEADSET_DIAGNOSTICS_LABEL)
        result2 = self.verify_element(TunesAppLocators.HEADSET_DIAGNOSTICS_BTN)
        return result1 and result2

    def verify_meeting_alerts_displayed(self) -> bool:
        """ Method to verify is Meeting Alerts label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.MEETING_ALERT_TITLE)

    def verify_hi_speed_usb_30_displayed(self) -> bool:
        """ Method to verify is Hi-Speed USB 3.0 label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.HI_SPEED_USB_TITLE)

    def verify_reconnecting_device_label_displayed(self):
        """Method to verify is Reconnecting device label is displayed

        @return: True if label is displayed, False otherwise

        """
        return self.verify_element(TunesAppLocators.LOGI_DOCK_RECONNECTING_DIALOG)

    def verify_ringtone_diagnostics_displayed(self) -> bool:
        """ Method to verify ringtone diagram in headset diagnostics is displayed.

        @return: True if ringtone diagram is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.HEADSET_DIAGNOSTICS_RINGTONE_DIAGRAM)

    def verify_headset_diagnostics_result(self, expected_mic_and_speaker_workable=True,
                                          expected_headset_connected=True) -> bool:
        """ Method to verify headset diagnostics result shows right result to the user

        @return: True if the result is correct
        """
        result = None
        if expected_mic_and_speaker_workable:
            result = self.verify_element(TunesAppLocators.HEADSET_DIAGNOSTICS_MIC_SPEAKER_OK_LABEL)
        else:
            result = self.verify_element(TunesAppLocators.HEADSET_DIAGNOSTICS_MIC_SPEAKER_BROKEN_LABEL)

        if expected_headset_connected:
            result = result and self.verify_element(TunesAppLocators.HEADSET_DIAGNOSTICS_CONNECTIVITY_LABEL)

        result = result and self.verify_element(TunesAppLocators.HEADSET_DIAGNOSTICS_SOFTPHONE_LABEL)
        return result

    def verify_rotate_to_mute_label_displayed(self) -> bool:
        """ Method to verify is Rotate to mute label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.ROTATE_TO_MUTE_LABEL)

    def verify_noise_cancellation_displayed(self) -> bool:
        """ Method to verify is Noise cancelaltion label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.NOISE_CANCELLATION_LABEL)

    def verify_voice_prompts_displayed(self) -> bool:
        """ Method to verify is Voice Prompts label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.VOICE_PROMPTS_LABEL)

    def verify_voice_prompts_3_levels_displayed(self) -> bool:
        """ Method to verify is Voice Prompts label is displayed. Applied for Cybermoprh headsets.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.VOICE_PROMPTS_3_LEVEL_LABEL)

    def verify_anc_group_button_displayed(self) -> bool:
        """ Method to verify is ANC Button Group label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.ANC_BUTTON_GROUP)

    def verify_health_and_safety_displayed(self) -> bool:
        """ Method to verify is Health and Safety label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.HEALTH_AND_SAFETY_LABEL)

    def verify_on_head_detection_displayed(self) -> bool:
        """ Method to verify is On Head Detection label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.ON_HEAD_DETECTION_LABEL)

    def verify_auto_mute_displayed(self) -> bool:
        """ Method to verify is Auto Mute label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.AUTO_MUTE_LABEL)

    def verify_auto_answer_displayed(self) -> bool:
        """ Method to verify is Auto Answer label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.AUTO_ANSWER_LABEL)

    def verify_auto_pause_displayed(self) -> bool:
        """ Method to verify is Auto Pause label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.AUTO_PAUSE_LABEL)

    def verify_anc_button_options_displayed(self) -> bool:
        """ Method to verify is ANC Button Options label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.ANC_BUTTON_OPTIONS)

    def verify_advanced_call_clarity_displayed(self) -> bool:
        """ Method to verify is Advanced Call Clarity label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.ADVANCED_CALL_CLARITY_LABEL)

    def verify_touch_pad_displayed(self) -> bool:
        """ Method to verify is Touch Pad label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.TOUCH_PAD_TITLE)

    def verify_personal_eq_displayed(self) -> bool:
        """ Method to verify is Touch Pad label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.PERSONAL_EQ_TITLE)

    def verify_headset_language_displayed(self) -> bool:
        """ Method to verify is Headset language label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.LANGUAGE_TITLE)

    def verify_device_name_label_displayed(self) -> bool:
        """ Method to verify is Device Name label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.DEVICE_NAME_MAIN_LABEL)

    def verify_sleep_settings_label_displayed(self) -> bool:
        """ Method to verify Sleep Settings label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.SLEEP_SETTINGS_LABEL)

    def verify_button_functions_label_displayed(self) -> bool:
        """ Method to verify Button functions label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.BUTTON_FUNCTIONS_LABEL)

    def verify_connection_priority_label_displayed(self) -> bool:
        """ Method to verify Connection priority label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.CONNECTION_PRIORITY_LABEL)

    def verify_connected_device_label_displayed(self) -> bool:
        """ Method to verify Connection priority label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.CONNECTED_DEVICES_LABEL)

    def verify_auto_focus_enable(self):
        return self.look_element(
            TunesAppLocators.ADJUSTMENTS_FOCUS_CHECKBOX).is_selected()

    def verify_color_filter_displayed(self, color_filter):
        return self.verify_element(TunesAppLocators.COLOR_FILTER_TITLE,
                                   timeunit=3,
                                   param=color_filter)

    def verify_power_on_displayed(self) -> bool:
        """ Method to verify is Power On label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.POWER_ON_TITLE)

    def verify_litra_temperature_title_displayed(self) -> bool:
        """ Method to verify is Temperature label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.LITRA_TEMPERATURE_TITLE)

    def verify_litra_temperature_slider_displayed(self) -> bool:
        """ Method to verify is Temperature slider is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.LITRA_TEMPERATURE_SLIDER)

    def verify_litra_brightness_title_displayed(self) -> bool:
        """ Method to verify is Brightness label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.LITRA_BRIGHTNESS_TITLE)

    def verify_litra_brightness_slider_displayed(self) -> bool:
        """ Method to verify is Brightness slider is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.LITRA_BRIGHTNESS_SLIDER)

    def verify_litra_brightness_up_enable(self) -> bool:
        """
        Method to check ability to click element
        """
        status = self.look_element(
            TunesAppLocators.LITRA_BRIGHTNESS_PLUS).get_attribute('disabled')
        Report.logInfo(f'Litra Brightness plus status is: {not status}.')
        return not status

    def verify_litra_temperature_up_enable(self) -> bool:
        """
        Method to check ability to click element
        """
        status = self.look_element(
            TunesAppLocators.LITRA_TEMP_PLUS).get_attribute('disabled')
        Report.logInfo(f'Litra Brightness plus status is: {not status}.')
        return not status

    def verify_litra_brightness_down_enable(self) -> bool:
        """
        Method to check ability to click element
        """
        status = self.look_element(
            TunesAppLocators.LITRA_BRIGHTNESS_MINUS).get_attribute('disabled')
        Report.logInfo(f'Litra Brightness plus status is: {not status}.')
        return not status

    def verify_litra_temperature_down_enable(self) -> bool:
        """
        Method to check ability to click element
        """
        status = self.look_element(
            TunesAppLocators.LITRA_TEMP_MINUS).get_attribute('disabled')
        Report.logInfo(f'Litra Brightness plus status is: {not status}.')
        return not status

    def verify_litra_power_warning(self) -> bool:
        """ Method to verify if power warning  is displayed.

        @return: True if warning is displayed, False otherwise
        """
        return self.verify_element((TunesAppLocators.LITRA_POWER_WARRNING))

    def verify_calendar_connect_now(self) -> bool:
        """ Method to verify if connect now label is displayed.
        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.CONNECT_NOW)

    def get_current_litra_temperature(self) -> int:
        """ Method to get current Litra light temperature.
        @return: Value in int
        """
        return int(self.look_element(TunesAppLocators.LITRA_TEMPERATURE_SLIDER).get_attribute('value'))

    def get_current_litra_brightness(self) -> int:
        """ Method to get current Litra light brightness.
        @return: Value in int
        """
        return int(self.look_element(TunesAppLocators.LITRA_BRIGHTNESS_SLIDER).get_attribute('value'))

    def get_current_litra_preset_name(self) -> str:
        preset_element = self.look_element_by_text(TunesAppLocators.LITRA_LABEL_NAME, 'Presets')
        preset_parent_element = preset_element.find_element(By.XPATH, '..').text
        preset_name_from_tune = ' '.join(preset_parent_element.split()[1:])
        return preset_name_from_tune

    def get_litra_min_defined_temperature(self) -> int:
        """
        Get litra minimal available temperature defined in Tune
        """
        return int(self.look_element(TunesAppLocators.LITRA_TEMPERATURE_SLIDER).get_attribute('min'))

    def get_litra_max_defined_temperature(self) -> int:
        """
        Get litra maximal available temperature defined in Tune
        """
        return int(self.look_element(TunesAppLocators.LITRA_TEMPERATURE_SLIDER).get_attribute('max'))

    def get_litra_min_defined_brightness(self) -> int:
        """
        Get litra minimal available brightness defined in Tune
        """
        return int(self.look_element(TunesAppLocators.LITRA_BRIGHTNESS_SLIDER).get_attribute('min'))

    def get_litra_max_defined_brightness(self) -> int:
        """
        Get litra maximal available temperature defined in Tune
        """
        return int(self.look_element(TunesAppLocators.LITRA_BRIGHTNESS_SLIDER).get_attribute('max'))

    def get_meeting_countdown_label_text(self, title: str) -> Optional[str]:
        """
        Get meeting countdown label with such information as: x min left, Now, in x min
        """
        regex_pattern_before = r'in \d{1,2} min'
        regex_pattern_after = r'\d{1,2} min left'

        meeting_cards = self.look_all_elements(TunesAppLocators.MEETING_CARD)

        for meeting in meeting_cards:
            if title in meeting.text:
                if 'Now' in meeting.text:
                    return 'Now'

                label = re.search(regex_pattern_before, meeting.text)
                if label:
                    return label.group()

                label = re.search(regex_pattern_after, meeting.text)
                if label:
                    return label.group()

        Report.logInfo('No labels with considered in the test text or no meeting card with given '
                       'title found or lack of meeting cards in current view')

    def get_meeting_time_duration_label_text(self, title: str) -> Optional[str]:
        """
        Get meeting time duration label with such information as: start time, end time
        """
        regex_pattern = r'\d{1,2}:\d{1,2} \w{1,2} - \d{1,2}:\d{1,2} \w{1,2}'
        meeting_cards = self.look_all_elements(TunesAppLocators.MEETING_CARD)
        for meeting in meeting_cards:
            if title in meeting.text:

                label = re.search(regex_pattern, meeting.text)
                if label:
                    return label.group()

        Report.logInfo('No labels with considered in the test text or no meeting card with given '
                       'title found or lack of meeting cards in current view')

    def get_join_button_text(self, title: str) -> str:
        """
        Get join button text with such information as: 'JOIN EARLY' or 'JOIN NOW'
        """
        meeting_cards = self.look_all_elements(TunesAppLocators.MEETING_CARD)

        for meeting in meeting_cards:
            if title in meeting.text:
                if 'JOIN EARLY' in meeting.text:
                    return 'JOIN EARLY'

                if 'JOIN NOW' in meeting.text:
                    return 'JOIN NOW'

        return 'No buttons or no meeting card with given title found or lack of meeting cards in current view'

    def open_litra_presets(self) -> None:
        """
        Method to open Litra presets
        """
        self.look_element_by_text(TunesAppLocators.LITRA_LABEL_NAME, 'Presets').click()

    def close_litra_presets(self) -> None:
        """
        Method to close Litra presets
        """
        self.look_element(TunesAppLocators.LITRA_PRESET_CLOSE).click()

    def close_litra_device_name_change(self) -> None:
        """
        Method to close Litra name change popup
        """
        self.look_element(TunesAppLocators.LITRA_DEVICE_NAME_POPUP_CLOSE).click()

    def click_litra_label_name(self, name: str) -> None:
        """
        Method to click Litra label
        @param name: label name, e.g. 'Device name' or 'Presets'
        """
        self.look_element_by_text(TunesAppLocators.LITRA_LABEL_NAME, name).click()

    def click_litra_device_name(self, name: str) -> None:
        """
        Method to click Litra label
        @param name: label name, e.g. 'Device name' or 'Presets'
        """
        self.look_element_by_text(TunesAppLocators.DEVICE_NAME_MAIN_LABEL, name).click()

    def click_litra_preset(self, preset_name: str) -> None:
        """
        Method to click preset name when window with presets is visible.
        @param preset_name: preset name as it is displayed in Tune
        """
        from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_litra_beam import \
            litra_beam_presets

        litra_radio = self.look_element_name('illuminationPresetOptions')
        radio_parent = litra_radio.find_element(By.XPATH, '../../..')
        radio_parent.find_element(By.XPATH,
            f'//div[@data-testid="settingsmenu.illuminationPreset.popup.{litra_beam_presets[preset_name]["testid"]}"]'
        ).click()
        time.sleep(1)

    def click_litra_temperature_up(self) -> None:
        """
        Method to click temperature up
        """
        self.look_element(TunesAppLocators.LITRA_TEMPERATURE_SLIDER).send_keys(Keys.ARROW_RIGHT)

    def click_litra_temperature_down(self) -> None:
        """
        Method to click temperature down
        """
        self.look_element(TunesAppLocators.LITRA_TEMPERATURE_SLIDER).send_keys(Keys.ARROW_LEFT)

    def click_litra_brightness_up(self) -> None:
        """
        Method to click brightness up
        """
        self.look_element(TunesAppLocators.LITRA_BRIGHTNESS_SLIDER).send_keys(Keys.ARROW_RIGHT)

    def click_litra_brightness_down(self) -> None:
        """
        Method to click brightness down
        """
        self.look_element(TunesAppLocators.LITRA_BRIGHTNESS_SLIDER).send_keys(Keys.ARROW_LEFT)

    def verify_adjustments_auto_white_balance_enable(self) -> bool:
        """Method to verfify Auto white Balance is selected

        @return: True is toggle is On, False otherwise
        """
        status = self.look_element(
            TunesAppLocators.ADJUSTMENTS_WHITE_BALANCE_CHECKBOX).is_selected()

        Report.logInfo(f'Auto White Balance status is {status}.')
        return status

    def verify_more_details_displayed(self):
        return self.verify_element(TunesAppLocators.MORE_DETAILS)

    def verify_factory_reset_displayed(self):
        return self.verify_element(TunesAppLocators.FACTORY_RESET)

    def verify_settings_hdr_enable(self):
        return self.look_element(TunesAppLocators.ADJUSTMENTS_HDR_CHECKBOX).is_selected()

    def verify_update_available_button(self):
        return self.verify_element(TunesAppLocators.UPDATE)

    def verify_built_in_mic_enable(self):
        return self.look_element(
            TunesAppLocators.BUILT_IN_MIC_TOGGLE).is_selected()

    def click_my_devices(self):
        e = self.look_element_by_text(TunesAppLocators.TAB, "Devices")
        if e.get_attribute('aria-selected') == 'false':
            e.click()

    def verify_reconnect_device(self):
        return self.verify_element(TunesAppLocators.RECONNECT_DEVICE)

    def verify_home(self):
        return self.verify_element(TunesAppLocators.HOME)

    def click_home(self):
        e = self.look_element(TunesAppLocators.HOME)
        self.click_by_script(e)

    def click_device(self, device_name):
        if device_name in STRICT_CHECK_DEVICES:
            self.look_element(TunesAppLocators.DEVICE_VER1, param=device_name).click()
        else:
            self.look_element(TunesAppLocators.DEVICE, param=device_name).click()

    def verify_device(self, device_name: str, status: bool) -> bool:
        locator = TunesAppLocators.DEVICE_VER1 if device_name in STRICT_CHECK_DEVICES else TunesAppLocators.DEVICE
        result = self.verify_element(locator, param=device_name, timeunit=15)

        if result == status:
            message = f'Device {device_name} has been verified in Logi Tune.' if status else f'Device {device_name} has not been detected in Logi Tune as expected.'
            Report.logInfo(message, screenshot=True)
            return True
        else:
            Report.logFail(f'Device {device_name} verification failed in Logi Tune.', screenshot=True)
            return False

    def click_back_button_cybermorph(self):
        self.look_element(TunesAppLocators.BACK_CYBERMORPH).click()

    def click_back_button_to_my_devices(self):
        self.look_element(TunesAppLocators.BACK_TO_MY_DEVICES).click()

    def click_back_button_to_device_settings(self):
        self.look_element(TunesAppLocators.BACK_TO_DEVICE_SETTINGS).click()

    def click_close_settings_screen(self):
        self.look_element(TunesAppLocators.CLOSE_SCREEN).click()

    def click_supported_devices(self):
        self.look_element(TunesAppLocators.SUPPORTED_DEVICES_LINK).click()

    def click_ok_button_on_supported_devices(self):
        self.look_element(TunesAppLocators.SUPPORTED_DEVCES_OK_BUTTON).click()

    def click_zoom_in(self):
        for x in range(5):
            UIBase.elementName = "Zoom In"
            self.look_element(TunesAppLocators.ZOOM_SLIDER).send_keys(Keys.ARROW_RIGHT)

    def click_zoom_out(self):
        for x in range(5):
            UIBase.elementName = "Zoom Out"
            self.look_element(TunesAppLocators.ZOOM_SLIDER).send_keys(Keys.ARROW_LEFT)

    def click_pan_left(self):
        for x in range(2):
            UIBase.elementName = "Pan Left"
            self.look_element(TunesAppLocators.PAN_LEFT).click()

    def click_pan_right(self):
        for x in range(2):
            UIBase.elementName = "Pan Right"
            self.look_element(TunesAppLocators.PAN_RIGHT).click()

    def click_tilt_up(self):
        for x in range(2):
            UIBase.elementName = "Tilt Up"
            self.look_element(TunesAppLocators.TILT_UP).click()

    def click_tilt_down(self):
        for x in range(2):
            UIBase.elementName = "Tilt Down"
            self.look_element(TunesAppLocators.TILT_DOWN).click()

    def click_image_adjustment(self):
        self.look_element(TunesAppLocators.IMAGE_ADJUSTMENT_LABEL).click()

    def click_adjustments_tab(self):
        self.look_element(TunesAppLocators.COLOR_ADJUSTMENTS_TAB).click()

    def click_color_filters_tab(self):
        self.look_element(TunesAppLocators.COLOR_FILTERS_TAB).click()

    def click_color_filter(self, filter):
        self.look_element(TunesAppLocators.COLOR_FILTER_TITLE, filter).click()

    def click_adjustments_reset_to_default(self):
        time.sleep(1)
        self.look_element(
            TunesAppLocators.ADJUSTMENTS_RESET_TO_DEFAULT, scroll_flag=False).click()

    def click_adjustments_dropdown_button(self):
        self.look_element(TunesAppLocators.ADJUSTMENTS_INTERACTIVE_SCROLLBAR).click()

    def click_info_button(self):
        self.look_element(TunesAppLocators.INFO_BUTTON).click()

    def click_back_from_image_adjustments(self):
        self.look_element(TunesAppLocators.IMAGE_ADJUSTMENTS_BACK_BUTTON).click()

    def click_connected_devices(self) -> None:
        """ Method to click on Connected devices button

        @return: None
        """
        time.sleep(1)
        self.look_element(TunesAppLocators.CONNECTED_DEVICES_LABEL).click()

    def click_factory_reset(self):
        time.sleep(1)
        self.look_element(TunesAppLocators.FACTORY_RESET).click()

    def click_proceed_to_factory_reset(self):
        time.sleep(1)
        self.look_element(TunesAppLocators.PROCEED_TO_FACTORY_RESET).click()

    def click_update_button(self):
        self.look_element(TunesAppLocators.UPDATE).click()

    def click_start_update_button(self):
        self.look_element(TunesAppLocators.START_UPDATE).click()

    def click_done_button(self):
        self.look_element(TunesAppLocators.FWU_DONE, timeout=240).click()

    def get_adjustments_brightness_slider_value(self):
        time.sleep(1)
        element = self.look_element(
            TunesAppLocators.ADJUSTMENTS_BRIGHTNESS_SLIDER)
        return element.get_attribute("value")

    def get_adjustments_contrast_slider_value(self):
        time.sleep(1)
        element = self.look_element(
            TunesAppLocators.ADJUSTMENTS_CONTRAST_SLIDER)
        return element.get_attribute("value")

    def get_adjustments_saturation_slider_value(self):
        time.sleep(1)
        element = self.look_element(
            TunesAppLocators.ADJUSTMENTS_SATURATION_SLIDER)
        return element.get_attribute("value")

    def get_adjustments_sharpness_slider_value(self):
        time.sleep(1)
        element = self.look_element(
            TunesAppLocators.ADJUSTMENTS_SHARPNESS_SLIDER)
        return element.get_attribute("value")

    def capture_video_stream(self, name=None):
        time.sleep(5)
        element = self.look_element(TunesAppLocators.VIDEO_STREAM)
        return Report.get_element_screenshot(element, name)

    def get_firmware_update_available_version(self):
        time.sleep(1)
        element = self.look_element(TunesAppLocators.UPDATE_VERSION)
        version = str(element.text).split(" ")
        return version[len(version) - 1]

    def get_firmware_version(self):
        time.sleep(1)
        element = self.look_element(TunesAppLocators.FIRMWARE_VERSION_BOX)
        version = str(element.text).split(" ")
        return version[len(version) - 1]

    def is_device_label_displayed(self, device_name):
        device_name = (TunesAppLocators.DEVICE_NAME[0],
                       "//p[text()='{}']".format(device_name))
        self.look_element(device_name).click()
        self.look_element(device_name).click()
        self.look_element(TunesAppLocators.CONNECTED).click()

    def verify_coily_is_detected(self, device_name):
        time.sleep(3)
        Report.logInfo('Verify if "Logi Dock Flex" is detected in Logi Tune.')
        device_name_element = (TunesAppLocators.DEVICE_NAME[0], f"//p[text()='{device_name}']")
        if self.verify_element(device_name_element):
            Report.logPass(f"{device_name} is detected in Logi Tune.", screenshot=True, is_collabos=False)
        else:
            Report.logFail(f"{device_name} is not detected in Logi Tune.", is_collabos=False)

    def verify_coily_is_disconnected(self, device_name):
        Report.logInfo('Verify if "Logi Dock Flex" is disconnected from the LogiTune.')
        device_name_element = (TunesAppLocators.DEVICE_NAME[0], f"//p[text()='{device_name}']")
        if self.verify_element_not_visible(device_name_element, timeunit=10):
            Report.logPass(f"{device_name} is disconnected from Logi Tune", screenshot=True, is_collabos=False)
        else:
            Report.logFail(f"{device_name} is still visible in Logi Tune.", is_collabos=False)

    def verify_coily_peripherals_are_detected(self, connected_devices):
        if connected_devices is None:
            Report.logInfo("User did not connect any peripherals to Coily.")
        else:
            time.sleep(1)
            for device_name in connected_devices:
                Report.logInfo(
                    f"Verify if Coily peripheral: '{device_name}' is detected in Logi Tune.")
                device_name_element = (
                TunesAppLocators.DEVICE_NAME[0], f"//p[text()='{device_name}']")
                if self.verify_element(device_name_element):
                    Report.logPass(f"{device_name} is detected in Logi Tune.", screenshot=True,
                                   is_collabos=False)
                else:
                    Report.logFail(f"{device_name} is not detected in Logi Tune.", is_collabos=False)

    def verify_coily_peripherals_are_disconnected(self, connected_devices):
        if connected_devices is None:
            Report.logInfo("User did not connect any peripherals to Coily.")
        else:
            time.sleep(1)
            for device_name in connected_devices:
                Report.logInfo(
                    f"Verify if Coily peripheral: '{device_name}' is NOT detected in Logi Tune.")
                device_name_element = (
                TunesAppLocators.DEVICE_NAME[0], f"//p[text()='{device_name}']")
                if not self.verify_element(device_name_element, timeunit=2):
                    Report.logPass(f"{device_name} is disconnected from Logi Tune", screenshot=True,
                                   is_collabos=False)
                else:
                    Report.logFail(f"{device_name} is detected in Logi Tune.", is_collabos=False)

    def check_peripherals_for_unauthorized_user(self, connected_devices,
                                                never_block_peripherals=NEVER_BLOCK_PERIPHERALS):
        if never_block_peripherals:
            self.verify_coily_peripherals_are_detected(connected_devices)
        else:
            self.verify_coily_peripherals_are_disconnected(connected_devices)

    def open_my_devices_tab(self):
        # Check if current position is at MY DEVICES page, if not, click it
        if ((self.look_element(TunesAppLocators.MY_DEVICES).get_attribute("tabindex")) != '0'):
            self.look_element(TunesAppLocators.MY_DEVICES).click()

    def click_on_device_by_name(self, device_name: str):
        device_name_locator = (
            TunesAppLocators.DEVICE_NAME[0], f"//p[contains(., '{device_name}')]")
        el = self.look_element(device_name_locator)
        el.click()

    def verify_device_connected_by_name(self, device_name: str, timeout: int = 10):
        device_name_locator = (
            TunesAppLocators.DEVICE_NAME[0], f"//p[contains(., '{device_name}')]")
        return self.verify_element(device_name_locator, timeunit=timeout)

    @staticmethod
    def power_on_zone950(is_svc_lab):
        try:
            device_name = "Zone 950"
            pid = 0x0AFB
            usage_page = 65280
            hid_command = UsbHidCommunicationBase(device_name=device_name)
            Report.logInfo(f"Send Power ON command to {device_name}.")
            if is_svc_lab:
                connect_device('Zone 950 Charge')
                time.sleep(2)
            hid_command.write_power_on_command(pid=pid, usage_page=usage_page)
            time.sleep(10)
        except:
            print("")

    def open_device_in_my_devices_tab(self, device_name: str, skip_exception: bool = False):
        try:
            self.look_element(TunesAppLocators.MY_DEVICES, timeout=10, skip_exception=True).click()
        except (AttributeError, ElementClickInterceptedException):
            Report.logInfo("My Devices ALREADY CHOSEN!")
        try:
            self.click_on_device_by_name(device_name)
            self.check_if_update_required_occurred(device_name)
        except (AttributeError, ElementClickInterceptedException) as e:
            if skip_exception:
                Report.logInfo(f"{device_name} ALREADY CHOSEN!")
            else:
                raise e

    def check_if_update_required_occurred(self, device_name: str):
        if self.verify_element(TunesAppLocators.UPDATE_REQUIRED_LABEL, timeunit=2):
            Report.logInfo(f'Update Required shown for {device_name}, proceeding with update')
            self.update_required_handle(device_name)

    def update_required_handle(self, device_name: str, timeout: int = 500):
        try:
            self.look_element(TunesAppLocators.FW_UPDATE_UPDATE_BTN).click()
            self.look_element(TunesAppLocators.START_UPDATE).click()
            self.look_elements(TunesAppLocators.FWU_DONE, TunesAppLocators.UPDATE_FAILED,
                               timeout=timeout).click()
            self.click_on_device_by_name(device_name)
        except Exception as e:
            Report.logException(f'Issue occurred while trying to handle update required: {e}')

    def open_about_the_device(self, device_name: Optional[str] = None):
        if device_name and ("Brio" in device_name or "C9" in device_name):
            time.sleep(10)
        if self.verify_element(TunesAppLocators.INFO_BUTTON, timeunit=3):
            self.look_element(TunesAppLocators.INFO_BUTTON).click()
        if device_name and ("Brio" in device_name or "C9" in device_name):
            time.sleep(10)

    def open_languages_tab(self):
        try:
            self.look_element(TunesAppLocators.LANGUAGE_TAB, timeout=3, skip_exception=True).click()
        except AttributeError:
            Report.logInfo("Language tab ALREADY CHOSEN!")

    def get_current_language_name(self) -> str:
        """ Method to get current language name from Settings page

        @return: language name
        """
        element = self.look_element(TunesAppLocators.LANGUAGE_NAME_SETTINGS_TAB)
        Report.logInfo(f"Current Language name is {element.wrapped_element.text}")
        return element.wrapped_element.text

    def start_update_from_device_tab(self, device_name: str, timeout: int = 180) -> Tuple[str]:
        """Updates device via OTA update

        Clicks through UI to be able to run OTA flash and starts the update

        Args:
            device_name: A string providing name of the device
            timeout: An integer providing time in seconds after which update should time out
              (default 180)

        Returns:
            A tuple providing strings with firmware versions after flash
        """
        self._delete_config_file_if_exists()
        if self.verify_element(TunesAppLocators.FW_UPDATE_REQUIRED, timeunit=3):
            self.look_element(TunesAppLocators.FW_UPDATE_UPDATE_BTN).click()
            self.start_performance_test()
            self.look_element(TunesAppLocators.START_UPDATE).click()
            self.look_elements(TunesAppLocators.FWU_DONE, TunesAppLocators.UPDATE_FAILED,
                               timeout=timeout).click()
            self.end_performance_test(device_name)
        else:
            self.start_performance_test()
            self.look_element(TunesAppLocators.UPDATE).click()
            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(10)
            self.look_element(TunesAppLocators.START_UPDATE).click()
            self.look_elements(TunesAppLocators.FWU_DONE, TunesAppLocators.UPDATE_FAILED,
                               timeout=timeout).click()
            self.end_performance_test(device_name)

        firmware_version = self.check_firmware_version(device_name, skip_exception=True)
        return tuple(firmware_version.split('\n'))

    def start_language_update(self, language_download_locator: Tuple[str, str],
                              timeout: int = 1000) -> None:
        result = re.search("LANGUAGE_(.*)']/", language_download_locator[1])
        language = result.group(1)
        if self.verify_element(TunesAppLocators.LANGUAGE_TAB_HEADER, timeunit=1):
            if self.verify_element(language_download_locator, timeunit=1):
                self.look_element(language_download_locator).click()
                self.start_performance_test()
                self.look_element(TunesAppLocators.LANGUAGE_INSTALL).click()
                self.look_elements(TunesAppLocators.LANGUAGE_DONE, TunesAppLocators.UPDATE_FAILED,
                                   timeout=timeout).click()
                self.end_performance_test(f'{language} language download')
            else:
                Report.logInfo(f"Language {language} cannot be downloaded")
                raise ValueError
        else:
            Report.logInfo(f"Current tab is not Language one!")
            raise selenium.common.exceptions.ElementNotVisibleException

    def verify_language_update_success(self, language_radio_locator: Tuple[str, str]):
        result = re.search("LANGUAGE_(.*)']/", language_radio_locator[1])
        language = result.group(1)
        try:
            self.look_element(TunesAppLocators.LANGUAGE_TAB, timeout=3, skip_exception=True).click()
        except AttributeError:
            Report.logInfo("Language tab ALREADY CHOSEN!")
        try:
            radio_checked = self.look_element(language_radio_locator).get_attribute('checked')
            if radio_checked:
                Report.logInfo(f'{language} language was installed successfully!')
            else:
                Report.logFail(f'{language} language was NOT installed successfully!')
                raise unittest.TestCase.failureException
        except Exception as ex:
            Report.logException(ex)
            raise ex

    def click_update_logitune_now(self):
        Report.logInfo('Trying to get Successful Tune app update OK button', screenshot=True)
        app_update_button_ok = self.look_element(TunesAppLocators.TUNE_UPDATED_OK_BUTTON,
                                                 wait_for_visibility=True, skip_exception=True)
        if app_update_button_ok:
            app_update_button_ok.click()

        Report.logInfo('Trying to get Update Tune app button', screenshot=True)
        app_update_button = self.look_element(TunesAppLocators.UPDATE_APP_NOW,
                                              wait_for_visibility=True, skip_exception=True)
        if app_update_button:
            app_update_button.click()
        else:
            Report.logInfo('Trying to update Tune app via settings tab', screenshot=True)
            self.look_element(TunesAppLocators.SETTINGS_BUTTON).click()
            self.look_element(TunesAppLocators.ABOUT_TUNE_MENU).click()
            self.look_element(TunesAppLocators.UPDATE_APP_BUTTON).click()

    def update_firmware_with_easter_egg(self, device_file_path: str, device_name: str,
                                        is_receiver: bool = False, timeout: int = 500,
                                        is_persistency_test: bool = False) -> str:
        """Updates firmware via Easter Egg.

        Verifies binary file existence, clicks through UI to be able to run Easter Egg flash
        and starts the update.

        Args:
            device_file_path: A string with file path to binary file
            device_name: A string providing name of the device
            is_receiver: If True binary file path will be pasted into receiver input of Easter Egg
              (default False)
            timeout: An integer providing time in seconds after which update should time out
              (default 180)

        Returns:
            A string with firmware versions of device/receiver (if available) after flashing
        """
        verify_file_existence(device_file_path)
        self._create_config_file_if_not_exists()

        tune_settings = TuneAppSettings()
        current_flags = tune_settings.check_settings_file_flags('automate',
                                                                'easterEgg')
        flags_ok = all(current_flags.values())
        if not flags_ok:
            tune_settings.modify_settings_flags(automate=True,
                                                easterEgg=True)
            self.open_tune_app()
            self.open_device_in_my_devices_tab(device_name)
            self.open_about_the_device(device_name)
        
        if self.verify_element(TunesAppLocators.FW_UPDATE_REQUIRED, timeunit=3):
            self.look_element(TunesAppLocators.FW_UPDATE_UPDATE_BTN).click()
            self.look_element(TunesAppLocators.START_UPDATE).click()
            self.look_elements(TunesAppLocators.FWU_DONE, TunesAppLocators.UPDATE_FAILED,
                               timeout=timeout).click()

        elif not self.verify_element(TunesAppLocators.FIRMWARE_VERSION):
            self.open_about_the_device()

        device = self.start_easter_egg(file_path=device_file_path, device_name=device_name,
                                       is_receiver=is_receiver, timeout=timeout,
                                       is_persistency_test=is_persistency_test)
        return device

    def is_same_version(self, device_name: str,
                        device_expected_version: str,
                        receiver_expected_version: Optional[str] = None) -> Dict[str, bool]:
        """Checks if device has already needed version.

        Args:
            device_expected_version: A string with device expected version
            receiver_expected_version: An optional string with receiver expected version
              (default None)

        Returns:
            A dict with booleans which states if device and receiver versions are same
        """
        result = dict()
        device_actual_version_str = self.look_element(TunesAppLocators.FIRMWARE_VERSION
                                                      ).wrapped_element.text
        if device_name == "C930e" and "8.1." in device_actual_version_str:
            assert False, Report.logFail("Wrong hardware version for C930e camera.")

        device_actual_version = device_actual_version_str.split('\n')
        result['device'] = self.validate_versions(device_expected_version, device_actual_version[0])
        Report.logInfo(f"Current headset version ({device_actual_version[0]}) "
                       f"same as needed ({device_expected_version})?: {result['device']}")
        if receiver_expected_version is not None:
            result['receiver'] = self.validate_versions(receiver_expected_version,
                                                        device_actual_version[1])
            Report.logInfo(f"Current receiver version ({device_actual_version[1]}) "
                           f"same as needed ({receiver_expected_version})?: {result['receiver']}")

        return result

    @staticmethod
    def validate_versions(expected: str, observed: str, eeprom_validation: bool = False) -> bool:
        """Validate if expected firmware version is same or similar to observed

        Args:
            expected: A string providing expected firmware version
            observed: A string providing observed firmware version
            eeprom_validation: True if provided versions are EEPROM versions

        Returns: bool
        """
        pattern = re.compile(r"(?:\d\.)+\d")

        expected_found = re.search(pattern, expected)
        observed_found = re.search(pattern, observed)

        expected_parsed = expected_found.group(0) if expected_found else None
        observed_parsed = observed_found.group(0) if observed_found else None
        if not expected_parsed or not observed_parsed:
            raise Exception(f"No version parsed from expected: {expected} and observed: {observed}")

        return Comparator.compare_versions(expected_parsed, observed_parsed) == 0

    def start_easter_egg(self, file_path: str, device_name: str,
                         is_receiver: bool = False, timeout: int = 180,
                         is_persistency_test: bool = False) -> str:
        """Runs Easter Egg update of provided device.

        Args:
            file_path: A string with file path to binary file
            device_name: A string providing name of the device
            is_receiver: If True binary file path will be pasted into receiver input of Easter Egg
              (default False)
            timeout: An integer providing time in seconds after which update should time out
              (default 180)

        Returns:
            A string with firmware versions of device/receiver (if available) after flashing
        """
        if is_receiver:
            easter_egg_path_element = TunesAppLocators.RECEIVER_PATH_EASTER_EGG
            easter_egg_update_button_element = TunesAppLocators.RECEIVER_EASTER_EGG_UPDATE
        else:
            easter_egg_path_element = TunesAppLocators.DEVICE_PATH_EASTER_EGG
            easter_egg_update_button_element = TunesAppLocators.DEVICE_EASTER_EGG_UPDATE
        Report.logInfo("Take a screenshot on About the .. page before the update", screenshot=True)
        actions = ActionChains(global_variables.driver)
        if get_custom_platform() == "windows":
            actions.key_down(Keys.CONTROL)
        else:
            actions.key_down(Keys.COMMAND)
        actions.click(self.look_element(TunesAppLocators.EASTER_EGG_MENU_OPEN).wrapped_element)
        actions.perform()

        time.sleep(2)
        element = self.look_element(easter_egg_path_element)
        element.click()
        element.clear()
        element.send_keys(file_path)
        time.sleep(1)
        element.clear()
        Report.logInfo(f"Path: {file_path}")
        element.send_keys(file_path)  # it is required by macos to put path file twice

        self.look_element(TunesAppLocators.EASTER_EGG_TITLE).click()

        time.sleep(5)

        self.look_element(easter_egg_update_button_element).click()
        self.look_elements(TunesAppLocators.FWU_DONE, TunesAppLocators.UPDATE_FAILED,
                           timeout=timeout).click()
        return self.check_firmware_version(device_name, skip_exception=True, is_persistency_test=is_persistency_test)

    def check_firmware_version(self, device_name, skip_exception=False, is_persistency_test=False):
        if not self.verify_element(TunesAppLocators.FIRMWARE_VERSION):
            if is_persistency_test:
                time.sleep(5)
                self.open_device_in_my_devices_tab(device_name, skip_exception=skip_exception)
                time.sleep(5)
                self.open_about_the_device()
            else:
                self.open_device_in_my_devices_tab(device_name, skip_exception=skip_exception)
                self.open_about_the_device()

        return self.look_element(TunesAppLocators.FIRMWARE_VERSION).wrapped_element.text

    # the ... button
    def click_tune_menu(self):
        self.look_element(TunesAppLocators.SETTINGS_BUTTON).click()

    def verify_tune_sync_connected(self) -> bool:
        return self.verify_element(TunesAppLocators.ABOUT_CONNECTED, timeunit=120)

    def verify_tune_does_not_display_sync_connection_status(self) -> bool:
        return not self.verify_element(TunesAppLocators.ABOUT_CONNECTED, timeunit=30)

    def click_about_menu(self):
        self.look_element(TunesAppLocators.ABOUT_MENU).click()
        from testsuite_tune_app.tune_menu.pages.about_menu_page import AboutMenuPage
        return AboutMenuPage()

    def click_quit_menu(self):
        self.look_element(TunesAppLocators.QUIT_MENU).click()

    def is_device_battery_displayed(self, device_name):
        device_name = (TunesAppLocators.DEVICE_NAME[0],
                       "//p[text()='{}']".format(device_name))
        self.look_element(device_name).click()
        battery_ele = self.look_element(TunesAppLocators.BATTERY_SIGN)
        battery_ele_txt = battery_ele.wrapped_element.text
        self.assertTrue('%' in battery_ele_txt)

    def click_connect_now(self):
        """
        Method to click on Connect now link under Home
        :return none
        """
        self.look_element(TunesAppLocators.CONNECT_NOW).click()

    def click_sign_in(self):
        """
        Method to click on Sign in to Work account under Home
        :return none
        """
        self.look_element(TunesAppLocators.SIGN_IN).click()

    def click_privacy_box_in_work_account(self):
        """
        Method to click on Privacy Box account under Home
        :return none
        """
        self.look_element(TunesAppLocators.PRIVACY_ENABLE_BOX).click()

    def verify_sign_int_button_is_displayed(self):
        """
        Method to verify if 'Sign-in' is displayed.
        :return none
        """
        status = self.verify_element(TunesAppLocators.SIGN_IN, timeunit=3)
        Report.logInfo(f"Verify if 'Sign in' button is displayed.", screenshot=True)
        return status

    def click_google(self):
        """
        Method to click on Google image to connect to calendar
        :return none
        """
        self.look_element(TunesAppLocators.GOOGLE).click()

    def click_google_work_account(self):
        """
        Method to click on Google image to connect to calendar
        :return none
        """
        self.look_element(TunesAppLocators.GOOGLE_WORK_ACCOUNT).click()

    def click_logitech_desk_booking(self):
        """
        Method to click on Google image to connect to calendar
        :return none
        """
        time.sleep(1)
        self.look_element(TunesAppLocators.CONTINUE_DESK_BOOKING).click()
        time.sleep(1)
        self.look_element(TunesAppLocators.BASECAMP_SEARCH).click()
        time.sleep(1)
        self.look_element(TunesAppLocators.BASECAMP_SEARCH).send_keys(COILY_BASECAMP_NAME)
        time.sleep(1)
        self.look_element(TunesAppLocators.BASECAMP_NAME).click()
        time.sleep(1)
        self.look_element(TunesAppLocators.CONTINUE_TEAMMATES).click()
        time.sleep(1)
        self.look_element(TunesAppLocators.DONE_ADD_TEAMMATES).click()


    def verify_meeting_title(self, meeting_title, timeout=None):
        """
        Method to verify meeting_title event displayed in Home
        :param meeting_title
        :return bool
        """
        return self.verify_element_by_text(TunesAppLocators.CALENDAR_MEETING_TITLE, meeting_title)

    def click_equalizer(self) -> None:
        """ Method to click on the Equalizer box

        @return: None
        """
        self.look_element(TunesAppLocators.EQUALIZER).click()

    def verify_equalizer_name(self, equalizer_name: str) -> bool:
        """ Method to verify equalizer name on the Sound page

        @param equalizer_name: equalizer mode name
        @return: None
        """
        current_value = self.look_element(TunesAppLocators.EQUALIZER_BOX_PROFILE_NAME)
        self.highLightElement(current_value)
        if equalizer_name in current_value.wrapped_element.text:
            Report.logPass("Equalizer value correctly displayed on Sound page")
            return True
        else:
            Report.logFail("Equalizer value NOT correctly displayed on Sound page")
            return False

    def get_equalizer_profile_name(self) -> int:
        """ Method to get Equalizer profile name from Sound page

        @return: value from the slider
        """
        element = self.look_element(TunesAppLocators.EQUALIZER_BOX_PROFILE_NAME)
        Report.logInfo(f"Current Equalizer profile name is {element.wrapped_element.text}")
        return element.wrapped_element.text

    def set_equalizer_profile(self, profile_name: str) -> None:
        """Method to click on eq profile name and accept it by pressing Back button

        @param profile_name: equalizer profile name
        @return: None
        """
        Report.logInfo(f"Set new Equalizer profile to {profile_name}")
        equalizer_element = "//h4[text()='{}']".format(profile_name)
        new_element = (By.XPATH, equalizer_element)
        self.look_element(new_element).click()
        self.look_element(TunesAppLocators.EQUALIZER_BACK).click()

    def click_headset_diagnostics(self) -> None:
        """ Method to click on the headset diagnostics button

        @return: None
        """
        self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_BTN).click()

    def click_if_ringtone_hearable(self, is_hearable=True) -> None:
        """ Method to click if user can hear the ringtone during headset diagnostics

        @return: None
        """
        if is_hearable:
            self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_SPEAKER_TEST_YES_BTN).click()
        else:
            self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_SPEAKER_TEST_NO_BTN).click()

    def click_if_record_hearable(self, is_hearable=True) -> None:
        """ Method to click if user can hear the record during headset diagnostics

        @return: None
        """
        if is_hearable:
            self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_MIC_TEST_YES_BTN).click()
        else:
            self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_MIC_TEST_NO_BTN).click()

    def click_headset_diagnostics_record_button(self) -> None:
        """ Method to click recording button during headset diagnostics

        @return: None
        """
        self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_RECORD_BTN).click()

    def click_headset_diagnostics_record_stop_button(self) -> None:
        """ Method to click stopping recording button during headset diagnostics

        @return: None
        """
        self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_RECORD_STOP_BTN).click()

    def click_headset_diagnostics_close_button(self) -> None:
        """ Method to click headset diagnostics close button, redirect user to headset page

        @return: None
        """
        self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_CLOSE_BTN).click()

    def click_sidetone(self) -> None:
        """ Method to click on Sidetone box

        @return: None
        """
        time.sleep(1)
        self.look_element(TunesAppLocators.SIDETONE_LABEL).click()

    def click_sidetone_done(self) -> None:
        """ Method to close Sidetone box

        @return: None
        """
        time.sleep(1)
        self.look_element(TunesAppLocators.SIDETONE_DONE).click()

    def click_back_to_device(self) -> None:
        """ Method to click return arrow to get back to device's main window.

        @return: None
        """
        time.sleep(1)
        self.look_element(TunesAppLocators.DEVICE_BACK).click()

    def click_button_functions_back(self) -> None:
        """ Method to click return arrow to get back to device's main window.

        @return: None
        """
        time.sleep(1)
        self.look_element(TunesAppLocators.DEVICE_BUTTON_FUNCTIONS_BACK).click()

    def get_sidetone_slider_value(self) -> int:
        """ Method to get value from Sidetone slider

        @return: value from the slider
        """
        slider = self.look_element(TunesAppLocators.SIDETONE_SLIDER)
        value = int(slider.get_attribute('value'))
        Report.logInfo(f"Current sidetone slider value is {value}%")
        return value

    def set_sidetone_slider(self, percentage: int) -> None:
        """ Method to set sidetone slider to specific value

        @param percentage: target value of the slider
        @return: None
        """
        Report.logInfo(f"Set sidetone slider value to {percentage}%")
        slider = self.look_element(TunesAppLocators.SIDETONE_SLIDER)
        slider_area = self.look_element(TunesAppLocators.SIDETONE_SLIDER_AREA)
        slider_width = slider_area.size['width']

        x_off = ((slider_width * percentage) / 100) - slider_width / 2

        act = ActionChains(global_variables.driver)
        act.click_and_hold(slider).move_to_element_with_offset(slider_area, x_off, 0).release()
        act.perform()

        time.sleep(1)

        self.look_element(TunesAppLocators.SIDETONE_DONE).click()

    def verify_sidetone_value(self, value: str) -> bool:
        """ Method to verify if slider value on the Sound page

        @param value: slider value
        @return: True if values match, False otherwise
        """
        current_value = self.look_element(TunesAppLocators.SIDETONE_VALUE)
        self.highLightElement(current_value)
        if value in current_value.wrapped_element.text:
            Report.logPass("Sidetone value correctly displayed on Sound page", True)
            return True
        else:
            Report.logFail("Sidetone value NOT correctly displayed on Sound page")
            return False

    def verify_mic_level_value(self, value: str, device_name: str) -> bool:
        """ Method to verify if mic level value on the Sound page

        @param value: mic level value
        @return: True if values match, False otherwise
        """
        current_value = self.look_element(TunesAppLocators.MIC_LEVEL_VALUE)
        self.highLightElement(current_value)
        current_value = int(current_value.wrapped_element.text.split("%")[0])

        # Limitation: some kind of normalization made by the zone headset, discussed with dev
        approximation_error = 5

        system_mic_input_name = {
            "Zone 900": "Zone 900 Receiver",
            "Zone Vibe 125": "Zone Vibe 125",
            "Zone Vibe 130": "Zone Vibe 130",
            "Zone Vibe Wireless": "Zone Vibe Wireless",
            "Zone Wireless": "Zone Wireless",
            "Zone Wireless Plus": "Zone Wireless Plus",
            "Logi Dock": "Logi Dock",
            "Zone Wireless 2": "Zone Wireless 2",
            "Zone 950": "Zone 950",
            "H570e Mono": "Logi H570e Mono",
            "H570e Stereo": "Logi H570e Stereo"
        }

        # System mic level comparison
        from subprocess import Popen, PIPE, check_output
        import re

        input_vol_int = None
        if get_custom_platform() == "windows":
            directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            exe_path = os.path.join(directory, 'drivers', 'SetVol.exe')
            if device_name == "Zone 900":
                device_name = system_mic_input_name.get(device_name)
            process = Popen(f'{exe_path} report device Headset Microphone ({device_name})',
                            stdout=PIPE, bufsize=1)
            for line in iter(process.stdout.readline, b''):
                print(f'line: {line}')
                if "Master volume level = " in line.decode("utf-8", errors='ignore'):
                    input_vol_int = int(
                        line.decode("utf-8").split("Master volume level = ", 1)[1])
            process.communicate()

        if get_custom_platform() == "macos":
            if device_name in system_mic_input_name.keys():
                if device_name in ["Zone Wireless 2", "Zone 950"]:
                    output_bytes = check_output(["SwitchAudioSource", "-t", "input", "-a"])
                    system_input_names = output_bytes.decode("utf-8").split('\n')
                    for x in system_input_names:
                        if device_name in x:
                            Popen(["SwitchAudioSource", "-t", "input", "-s", x]).wait()
                else:
                    Popen(["SwitchAudioSource", "-t", "input", "-s", system_mic_input_name.get(device_name)]).wait()

            batcmd = "osascript -e 'get volume settings'"
            result = check_output(batcmd, shell=True)
            Report.logInfo(f"device_name: {device_name}")
            Report.logInfo(f"osascript result: {result}")
            input_vol = re.split(',', str(result))[1]
            input_vol_int = int(re.search(r'\d+', input_vol).group())

        if input_vol_int:
            if abs(input_vol_int - current_value) <= approximation_error:
                Report.logInfo("Current Mic level on Tune matches system value")
            else:
                Report.logFail(
                    f"Current Mic level on Tune doesn't match system value: {current_value} != ({input_vol_int} +/- {approximation_error})")
                return False

        if int(value) - approximation_error <= current_value <= int(value) + approximation_error:
            Report.logPass("Mic level value correctly displayed on Sound page", True)
            return True
        else:
            Report.logFail(
                f"Mic level value NOT correctly displayed on Sound page: {current_value} != ({value} +/- {approximation_error})")
            return False

    def get_mic_level_slider_value(self) -> int:
        """ Method to get value from Mic level slider

        @return: value from the slider
        """
        slider = self.look_element(TunesAppLocators.MIC_LEVEL_SLIDER)
        value = int(slider.get_attribute('value'))
        Report.logInfo(f"Current Mic level slider value is {value}%")
        return value

    def set_mic_level_slider(self, percentage: int) -> None:
        """ Method to set Mic level slider to specific value

        @param percentage: target value of the slider
        @return: None
        """
        time.sleep(1)
        Report.logInfo(f"Set MIC LEVEL slider value to {percentage}%")
        slider = self.look_element(TunesAppLocators.MIC_LEVEL_SLIDER)
        slider_area = self.look_element(TunesAppLocators.MIC_LEVEL_SLIDER_AREA)
        slider_width = slider_area.size['width']

        x_off = ((slider_width * percentage) / 100) - slider_width / 2

        act = ActionChains(global_variables.driver)
        act.click_and_hold(slider).move_to_element_with_offset(slider_area, x_off, 0).release()
        act.perform()

        time.sleep(1)

        self.look_element(TunesAppLocators.MIC_LEVEL_DONE).click()

    def click_mic_level_done(self) -> None:
        """ Method to close Mic Level box

        @return: None
        """
        time.sleep(1)
        self.look_element(TunesAppLocators.MIC_LEVEL_DONE).click()

    def verify_device_name_value(self, name: str) -> bool:
        """ Method to verify Device Name on Settings Page

        @param name: device name
        @return: True if name match, False otherwise
        """
        current_value = self.look_element(TunesAppLocators.DEVICE_NAME_RENAME)
        self.highLightElement(current_value)
        if name in current_value.wrapped_element.text:
            Report.logPass("Device Name matches")
            return True
        else:
            Report.logFail("Device Name does not match")
            return False

    def click_rotate_to_mute_toggle(self) -> None:
        """ Method to click on the Rotate to Mute toggle

        @return: None
        """
        self.look_element(TunesAppLocators.ROTATE_TO_MUTE_TOGGLE).click()

    def get_rotate_to_mute_state(self) -> bool:
        """ Method to get state of Rotate to Mute toggle

        @return: state of the toggle
        """
        element = self.look_element(TunesAppLocators.ROTATE_TO_MUTE_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_touch_pad_toggle(self) -> None:
        """ Method to click on the Touch Pad toggle

        @return: None
        """
        self.look_element(TunesAppLocators.TOUCH_PAD_TOGGLE).click()

    def get_touch_pad_state(self) -> bool:
        """ Method to get state of Touch Pad toggle

        @return: state of the toggle
        """
        element = self.look_element(TunesAppLocators.TOUCH_PAD_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_voice_prompts_toggle(self) -> None:
        """ Method to click on the Voice prompts toggle

        @return: None
        """
        self.look_element(TunesAppLocators.VOICE_PROMPTS_TOGGLE).click()

    def click_voice_prompts_level_name(self) -> None:
        """ Method to click on the Voice prompts level name

        @return: None
        """
        self.look_element(TunesAppLocators.VOICE_PROMPTS_3_LEVEL_NAME).click()

    def choose_new_voice_prompt_level(self, level: str) -> None:
        """Method to click on the new voice prompt.

        @param level:
        @return:
        """
        child_locator = (By.XPATH, "//div[text()='{}']".format(level))
        child_element = self.look_element(child_locator)
        parent_element = child_element.find_element(By.XPATH, '..')
        parent_element = parent_element.find_element(By.XPATH, '..')

        radio_button = parent_element.find_element(By.CLASS_NAME, "input-container").wrapped_element
        actions = ActionChains(global_variables.driver)
        actions.move_to_element(radio_button).click().perform()
        time.sleep(1)
        self.look_element(TunesAppLocators.VOICE_PROMPTS_3_SAVE_DIALOG).click()

    def click_advance_call_clarity_level_name(self) -> None:
        """ Method to click on the Advanced Call Clarity level name

        @return: None
        """
        self.look_element(TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_NAME).click()

    def choose_new_advanced_call_clarity_level(self, level: str) -> None:
        """Method to click on the new advanced call clarity level.

        @param level:
        @return:
        """
        child_locator = (By.XPATH, "//div[text()='{}']".format(level))
        child_element = self.look_element(child_locator)
        parent_element = child_element.find_element(By.XPATH, '..')
        parent_element = parent_element.find_element(By.XPATH, '..')

        radio_button = parent_element.find_element(By.CLASS_NAME, "input-container").wrapped_element
        actions = ActionChains(global_variables.driver)
        actions.move_to_element(radio_button).click().perform()
        time.sleep(1)
        self.look_element(TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_SAVE_DIALOG).click()

    def click_advance_call_clarity_save(self) -> None:
        """ Method to click on the Advanced Call Clarity save button

        @return: None
        """
        self.look_element(TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_SAVE_DIALOG).click()

    def click_power_on_toggle(self) -> None:
        """ Method to click on the Power On toggle

        @return: None
        """
        self.look_element(TunesAppLocators.POWER_ON_TITLE_TOGGLE).click()

    def click_litra_beam_factory_reset_done_button(self) -> None:
        """ Method to click on the Done button in Litra Beam factory reset

        @return: None
        """
        self.look_element(TunesAppLocators.LITRA_FACTORY_RESET_DONE).click()

    def get_noise_cancellation_state(self) -> bool:
        """ Method to get state of the Nise cancellation toggle

        @return: state of the toggle
        """
        element = self.look_element(TunesAppLocators.NOISE_CANCELLATION_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_noise_cancellation_toggle(self) -> None:
        """ Method to click on the Noise Cancellation toggle

        @return: None
        """
        self.look_element(TunesAppLocators.NOISE_CANCELLATION_TOGGLE).click()

    def click_anc_button(self, button: Tuple) -> None:
        """ Method to click on the Noise Cancellation toggle

        @return: None
        """
        self.look_element(button).click()

    def verify_anc_button_active(self, button: Tuple) -> bool:
        """ Method to click on the Noise Cancellation toggle

        @return: None
        """
        attributes = self.look_element(button).get_attribute('class')
        return "icon-circlebackground" in attributes

    def click_anc_button_options(self) -> None:
        """ Method to click on the ANC Button Options.

        @return: None
        """
        self.look_element(TunesAppLocators.ANC_BUTTON_OPTIONS).click()

    def verify_anc_button_option_label_displayed(self, button: Tuple) -> bool:
        """ Method to check if ANC Button option is displayed

        @return: None
        """
        return self.verify_element(button)

    def get_anc_button_option_state(self, button: Tuple) -> bool:
        """ Method to get state of the ANC Button Option toggle

        @return: state of the toggle
        """
        element = self.look_element(button)
        return element.wrapped_element.is_selected()

    def click_anc_button_option_toggle(self, button: Tuple) -> None:
        """ Method to click on the ANC Button Option toggle

        @return: state of the toggle
        """
        self.look_element(button).click()

    def click_health_and_safety_label(self) -> None:
        """ Method to click on the Health and Safety label.

        @return: None
        """
        self.look_element(TunesAppLocators.HEALTH_AND_SAFETY_LABEL).click()

    def get_anti_startle_protection_state(self, is_dashboard_feature: bool = False) -> bool:
        """
        Args:
            is_dashboard_feature: (bool) Indicates whether the anti startle protection feature is accessed through the dashboard or not.

        Returns:
            (bool) The state of the anti startle protection feature. True if the checkbox is selected, False otherwise.
        """
        if is_dashboard_feature:
            element = self.look_element(TunesAppLocators.DASHBOARD_ANTI_STARTLE_PROTECTION_CHECKBOX)
        else:
            element = self.look_element(TunesAppLocators.ANTI_STARTLE_PROTECTION_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_anti_startle_protection_toggle(self, is_dashboard_feature: bool = False) -> None:
        """
        Toggle the anti startle protection feature.

        Args:
            is_dashboard_feature (bool): Optional. If True, the toggle element is located in the dashboard.
                                        If False (default), the toggle element is located outside the dashboard.

        Returns:
            None
        """
        if is_dashboard_feature:
            self.look_element(TunesAppLocators.DASHBOARD_ANTI_STARTLE_PROTECTION_TOGGLE).click()
        else:
            self.look_element(TunesAppLocators.ANTI_STARTLE_PROTECTION_TOGGLE).click()

    def get_noise_exposure_control_state(self) -> bool:
        """ Method to get state of the Noise exposure toggle

        @return: state of the toggle
        """
        element = self.look_element(TunesAppLocators.NOISE_EXPOSURE_CONTROL_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_noise_exposure_control_toggle(self) -> None:
        """ Method to click on the Noise exposure control toggle

        @return: state of the toggle
        """
        self.look_element(TunesAppLocators.NOISE_EXPOSURE_CONTROL_TOGGLE).click()

    def click_on_head_detection(self) -> None:
        """ Method to click on the On head detection label.

        @return: None
        """
        self.look_element(TunesAppLocators.ON_HEAD_DETECTION_LABEL).click()

    def get_auto_mute_state(self) -> bool:
        """ Method to get state of the Auto-Mute toggle

        @return: state of the toggle
        """
        element = self.look_element(TunesAppLocators.AUTO_MUTE_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_auto_mute_toggle(self) -> None:
        """ Method to click on the Auto-Mute control toggle

        @return: state of the toggle
        """
        self.look_element(TunesAppLocators.AUTO_MUTE_TOGGLE).click()

    def get_auto_answer_state(self) -> bool:
        """ Method to get state of the Auto-Answer toggle

        @return: state of the toggle
        """
        element = self.look_element(TunesAppLocators.AUTO_ANSWER_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_auto_answer_toggle(self) -> None:
        """ Method to click on the Auto-Answer control toggle

        @return: state of the toggle
        """
        self.look_element(TunesAppLocators.AUTO_ANSWER_TOGGLE).click()

    def get_auto_pause_state(self) -> bool:
        """ Method to get state of the Auto-Pause toggle

        @return: state of the toggle
        """
        element = self.look_element(TunesAppLocators.AUTO_PAUSE_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_auto_pause_toggle(self) -> None:
        """ Method to click on the Auto-Pause control toggle

        @return: state of the toggle
        """
        self.look_element(TunesAppLocators.AUTO_PAUSE_TOGGLE).click()

    def get_voice_prompts_state(self) -> bool:
        """ Method to get state on the Voice Prompts toggle.

        @return: toggle state
        """
        element = self.look_element(TunesAppLocators.VOICE_PROMPTS_CHECKBOX)
        return element.wrapped_element.is_selected()

    def get_voice_prompts_level_name(self) -> str:
        """ Method to get name of the Voice Prompts level.

        @return: voice prompts level name
        """
        element = self.look_element(TunesAppLocators.VOICE_PROMPTS_3_LEVEL_NAME)
        return element.wrapped_element.text

    def get_advanced_call_clarity_level_name(self) -> str:
        """ Method to get name of the Advanced Call Clarity level.

        @return: voice prompts level name
        """
        element = self.look_element(TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_NAME)
        return element.wrapped_element.text

    def get_power_on_state(self) -> bool:
        """ Method to get state on the Power ON toggle.

        @return: toggle state
        """
        element = self.look_element(TunesAppLocators.POWER_ON_TITLE_CHECKBOX)
        return element.wrapped_element.is_selected()

    def get_device_name_from_settings_page(self) -> str:
        """ Method to get device name from Settings page.

        @return: device name on Settings page
        """
        element = self.look_element(TunesAppLocators.DEVICE_NAME_RENAME)
        name = element.wrapped_element.text
        Report.logInfo(f"Device name on Settings page is {name}")
        return name

    def click_mic_level(self) -> None:
        """ Method to click on the Mic level box

        @return: None
        """
        self.look_element(TunesAppLocators.MIC_LEVEL_LABEL).click()

    def click_meeting_alerts_toggle(self) -> None:
        """ Method to click on the Meeting Alerts toggle.

        @return: None
        """
        self.look_element(TunesAppLocators.MEETING_ALERT_TOGGLE).click()

    def get_meeting_alerts_state(self) -> bool:
        """ Method to get state on the Meeting Alerts toggle.

        @return: toggle state
        """
        element = self.look_element(TunesAppLocators.MEETING_ALERT_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_hi_speed_usb_3_0_toggle(self) -> None:
        """ Method to click on the Hi-Speed USB 3.0 toggle.

        @return: None
        """
        self.look_element(TunesAppLocators.HI_SPEED_USB_TOGGLE).click()

    def get_hi_speed_usb_3_0_state(self) -> bool:
        """ Method to get state on the Hi-Speed USB 3.0 toggle.

        @return: toggle state
        """
        element = self.look_element(TunesAppLocators.HI_SPEED_USB_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_device_name_rename(self) -> None:
        """ Method to click on the Device Name on Settings Page.

        @return: None
        """
        self.look_element(TunesAppLocators.DEVICE_NAME_RENAME).click()

    def clear_device_name(self) -> None:
        """Method to clear the input box fo device name

        @return: None
        """
        el = self.look_element(TunesAppLocators.DEVICE_NAME_INPUT)
        el.click()

        if get_custom_platform() == "windows":
            el.send_keys(Keys.CONTROL + "a")
        else:
            el.send_keys(Keys.COMMAND + "a")

        el.send_keys(Keys.DELETE)

    def set_new_device_name(self, name: str) -> None:
        """Method to set a new device name in device name input box.

        @param name: new device name
        @return: None
        """
        el = self.look_element(TunesAppLocators.DEVICE_NAME_INPUT)
        el.click()
        el.send_keys(name)

        self.click_device_name_update()

    def click_device_name_surprise_me(self) -> None:
        """ Method to click on Surprise Me for Device Name.

        @return: None
        """
        self.look_element(TunesAppLocators.DEVICE_NAME_SURPRISE).click()

    def click_device_name_update(self) -> None:
        """ Method to click on Update button in Device Name popup.

        @return: None
        """
        self.look_element(TunesAppLocators.DEVICE_NAME_UPDATE).click()

    def get_device_name_error(self) -> str:
        """ Method to get an error name from Device Name popup

        @return: error name
        """
        time.sleep(1)
        return self.look_element(TunesAppLocators.DEVICE_NAME_ERROR).wrapped_element.text

    def get_update_button_state_on_device_name_popup(self) -> bool:
        """Method to get enable status for Update Button on device name popup.

        @return: True if button is enabled, False otherwise
        """
        return self.look_element(TunesAppLocators.DEVICE_NAME_UPDATE).is_enabled()

    def get_value_from_device_name_input(self) -> str:
        """ Method to get a name from Device Name input field.

        @return: device name
        """
        name = self.look_element(TunesAppLocators.DEVICE_NAME_INPUT)
        value = name.get_attribute('value')
        Report.logInfo(f"Device Name input field value is {value}.")
        return value

    def click_current_sleep_settings_timeout(self) -> None:
        """ Method to click on current Sleep timeout on Settings page.

        @return: None
        """
        self.look_element(TunesAppLocators.SLEEP_SETTINGS_VALUE).click()

    def choose_new_sleep_timeout(self, value: int) -> None:
        """Method to choose a sleep timeout value.

        @param value:  new sleep timeout value
        @return: None
        """
        Report.logInfo(f"Set sleep timeout to {value}.")
        input_element = self.look_element(TunesAppLocators.SLEEP_TIMEOUT_INPUT, param=str(value))
        input_element.click()
        Report.logInfo(f"Checking if radio button with value {value} is checked")
        is_radio_button_checked = input_element.is_selected()
        if is_radio_button_checked:
            Report.logInfo(f"Radio Button with value {value} is checked - OK", screenshot=True)
        else:
            Report.logException(f"Radio Button with value {value} is NOT checked")
        self.look_element(TunesAppLocators.SLEEP_TIMEOUT_SAVE).click()

    def get_current_sleep_settings_timeout(self) -> int:
        """Get current sleep timeout value from Settings page in minutes.

        @return: sleep timeout in minutes
        """
        element = self.look_element(TunesAppLocators.SLEEP_SETTINGS_VALUE)
        text = element.wrapped_element.text
        Report.logInfo(f"Sleep timeout value on Settings Page is: {text}")

        if "minutes" in text:
            values = text.split(" ")
            return int(values[0])
        elif "hour" in text:
            values = text.split(" ")
            return int(values[0]) * 60
        else:
            return 0

    def click_button_functions_label(self) -> None:
        """ Method to click on Button functions label on Settings page.

        @return: None
        """
        self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_LABEL).click()

    def click_single_press_label(self) -> None:
        """ Method to click on Single Press label on Settings page.

        @return: None
        """
        self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_SINGLE_PRESS_LABEL).click()

    def get_current_button_single_press_function(self) -> str:
        """Get current button single press function.

        @return: connection type
        """
        element = self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_SINGLE_PRESS_VALUE)
        self.highLightElement(element)
        text = element.wrapped_element.text
        Report.logInfo(f"Current Single Press function is: {text}")
        return text

    def click_double_press_label(self) -> None:
        """ Method to click on Double Press label on Settings page.

        @return: None
        """
        self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_DOUBLE_PRESS_LABEL).click()

    def get_current_button_double_press_function(self) -> str:
        """Get current button double press function.

        @return: connection type
        """
        element = self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_DOUBLE_PRESS_VALUE)
        self.highLightElement(element)
        text = element.wrapped_element.text
        Report.logInfo(f"Current Double Press function is: {text}")
        return text

    def click_long_press_label(self) -> None:
        """ Method to click on Long Press label on Settings page.

        @return: None
        """
        self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_LONG_PRESS_LABEL).click()

    def get_current_button_long_press_function(self) -> str:
        """Get current button double press function.

        @return: connection type
        """
        element = self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_LONG_PRESS_VALUE)
        self.highLightElement(element)
        text = element.wrapped_element.text
        Report.logInfo(f"Current Long Press function is: {text}")
        return text

    def choose_new_button_function(self, function: str) -> None:
        """Method to click on the new button function.

        @param function:
        @return:
        """
        Report.logInfo(f"Choose function: {function}")
        child_locator = (By.XPATH, "//h4[text()='{}']".format(function))
        child_element = self.look_element(child_locator)
        parent_element = child_element.find_element(By.XPATH, '..')

        radio_button = parent_element.wrapped_element
        actions = ActionChains(global_variables.driver)
        actions.move_to_element(radio_button).click().perform()
        time.sleep(1)
        self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_SAVE_BUTTON).click()

    def click_restore_defaults_button(self) -> None:
        """ Method to click on Restore defaults for button functions..

        @return: None
        """
        self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_RESTORE_DEFAULTS).click()
        self.look_element(TunesAppLocators.BUTTON_FUNCTIONS_RESTORE_DEFAULTS_CONFIRM).click()

    def get_current_connection_priority(self) -> str:
        """Get current connection priority value from Settings page.

        @return: connection type
        """
        element = self.look_element(TunesAppLocators.CONNECTION_PRIORITY_VALUE)
        text = element.wrapped_element.text
        Report.logInfo(f"Connection Priority value on Settings Page is: {text}")

        return text

    def click_current_connection_priority(self) -> None:
        """Method to click on current connection priority value on Settings page.

        @return: None
        """
        self.look_element(TunesAppLocators.CONNECTION_PRIORITY_VALUE).click()

    def choose_new_connection_priority(self, current_value: str) -> None:
        """Method to choose a new connection priority value.

        @param current_value: current connection priority value
        @return:  None
        """
        stable_connection = "Stable connection"
        sound_quality = "Sound quality"

        if current_value == stable_connection:
            Report.logInfo(f'Change connection priority to: {sound_quality}')
            element = self.look_element(TunesAppLocators.CONNECTION_PRIORITY_SOUND_QUALITY).wrapped_element
        else:
            Report.logInfo(f'Change connection priority to: {stable_connection}')
            element = self.look_element(TunesAppLocators.CONNECTION_PRIORITY_STABLE_CONNECTION).wrapped_element

        actions = ActionChains(global_variables.driver)
        actions.move_to_element(element).click().perform()

        save_element = self.look_element(TunesAppLocators.CONNECTION_PRIORITY_SAVE).wrapped_element
        actions.move_to_element(save_element).click().perform()

    def get_currently_connected_device(self) -> str:
        """Method to get a name of currently connected device.

        @return: name of connected device
        """
        element = self.look_element(TunesAppLocators.CONNECTED_DEVICES_NAME)
        text = element.wrapped_element.text
        Report.logInfo(f"Currently connected device is: {text}")

        return text

    def click_on_close_connected_device_page(self) -> None:
        """Method to click on currently conencted device on Settings page.

        @return: None
        """
        self.look_element(TunesAppLocators.CONNECTED_DEVICE_CLOSE).click()

    def move_disconnect_button_center(self):
        """
        Method to move disconnect button to the center position for clicking
        :return none
        """
        script = "var b = document.querySelector('button');" \
                 "b.setAttribute('style', 'margin-bottom: auto; margin-top: auto;');"
        self.driver.execute_script(script)

    def click_disconnect_button(self):
        """
        Method to click on Disconnect button to disconnect Google calendar
        :return none
        """
        self.look_element(TunesAppLocators.DISCONNECT_BUTTON).click()
        time.sleep(1)
        self.look_element(TunesAppLocators.DISCONNECT_ACCOUNT_BUTTON).click()

    def click_app_settings(self):
        """
        Method to click on App settings
        :return none
        """
        self.look_element(TunesAppLocators.APP_SETTINGS).click()

    def click_calendar_connection(self):
        """
        Method to click on Calendar connection
        :return none
        """
        self.look_element(TunesAppLocators.CALENDAR_CONNECTION).click()

    def click_calendar_and_meetings(self):
        """
        Method to click on Calendar and meetings
        :return none
        """
        self.look_element(TunesAppLocators.CALENDAR_AND_MEETINGS).click()

    def click_settings_connected_account(self):
        """
        Method to click on Calendar connection
        :return none
        """
        self.look_element(TunesAppLocators.WORK_ACCOUNT).click()

    def click_disable_calendar(self):
        """
        Method to click on Disable calendar
        :return none
        """
        self.look_element(TunesAppLocators.DISABLE_CALENDAR).click()

    def click_disable_and_relaunch_app(self):
        """
        Method to click on Disable and relaunch app
        :return none
        """
        self.look_element(TunesAppLocators.DISABLE_AND_RELAUNCH_APP).click()

    def click_enable_and_relaunch_app(self):
        """
        Method to click on Enable and relaunch app
        :return none
        """
        self.look_element(TunesAppLocators.ENABLE_AND_RELAUNCH_APP).click()

    def click_refresh_calendar_button(self):
        self.look_element(TunesAppLocators.REFRESH_CALENDAR).click()
        self.wait_and_check_the_presence_of_element(TunesAppLocators.REFRESHING_FINISHED_SIGN)
        time.sleep(1)

    def verify_calendar_not_connected(self):
        """
        Method to verify Calendar is not connected in Calendar connection
        :return bool
        """
        return self.verify_element(TunesAppLocators.CALENDAR_IS_NOT_CONNECT, timeunit=5)

    def click_outlook(self) -> None:
        """
        Method to click on Outlook image to connect to calendar
        :return none
        """
        self.look_element(TunesAppLocators.OUTLOOK).click()

    def click_outlook_work_account(self) -> None:
        """
        Method to click on Outlook image to connect to calendar
        :return none
        """
        self.look_element(TunesAppLocators.OUTLOOK_WORK_ACCOUNT).click()

    def verify_refresh_calendar_button(self):
        return self.verify_element(TunesAppLocators.REFRESH_CALENDAR)

    def verify_no_meeting_soon(self) -> None:
        """
        Method to verify Home shows No meeting soon
        :return bool
        """
        return self.verify_element(TunesAppLocators.NO_MEETING_SOON)

    def click_support(self) -> None:
        """
        Method to click Support button on menu button
        :return none
        """
        self.look_element(TunesAppLocators.SUPPORT).click()

    def click_share_feedback(self):
        """
        Method to click on Share feedback button on menu button
        :return none
        """
        self.look_element(TunesAppLocators.SHARE_FEEDBACK).click()

    def click_sound_back(self) -> None:
        """
        Method to click on back button on sound page
        :return none
        """
        self.look_element(TunesAppLocators.SOUND_BACK_BUTTON).click()

    def check_is_device_connected(self, device_name) -> bool:
        """
        Method to check if device is connected
        :return none
        """
        element = (By.XPATH, f"//p[text()='{device_name}']")
        if self.verify_element(element, timeunit=20):
            return True
        else:
            return False

    def verify_receiver_displayed(self) -> bool:
        """ Method to verify if Receiver is displayed for device.
        :return True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.RECEIVER)

    def get_tune_app_ver(self) -> str:
        """
        Method to get Tune version from Tune About page
        :return tune_ver
        """
        return str(self.look_element(TunesAppLocators.APP_VERSION).wrapped_element.text)

    def verify_update_ok_button(self) -> bool:
        """
        Method to verify if OK button is on popup window
        :return bool
        """
        return self.verify_element(TunesAppLocators.UPDATE_OK, timeunit=15)

    def click_update_ok_button(self) -> None:
        """
        Method to click UPDATE OK button is on popup window
        :return None
        """
        self.look_element(TunesAppLocators.UPDATE_OK).click()

    def click_logi_dock_pair_headset(self) -> None:
        """
        Method to click Pair headset in tune app
        :return None
        """
        self.look_element(TunesAppLocators.LOGI_DOCK_PAIR_HEADSET).click()

    def click_logi_dock_pair_continue_button(self) -> None:
        """
        Method to click continue button to pair headset with logi dock
        :return None
        """
        self.look_element(TunesAppLocators.LOGI_DOCK_CONTINUE_BTN).click()

    def click_logi_dock_pair_done_button(self) -> None:
        """
        Method to click done button to pair headset with logi dock
        :return None
        """
        self.look_element(TunesAppLocators.LOGI_DOCK_DONE_BTN).click()

    def click_logi_dock_unpair_headset(self) -> None:
        """
        Method to click unpair headset to unpair headset with logi dock
        :return None
        """
        self.look_element(TunesAppLocators.LOGI_DOCK_UNPAIR_HEADSET).click()

    def click_logi_dock_unpair_button(self) -> None:
        """
        Method to click unpair headset to unpair headset with logi dock
        :return None
        """
        self.look_element(TunesAppLocators.LOGI_DOCK_UNPAIR_BTN).click()

    def click_receiver_to_pair(self, receiver_name: str) -> None:
        """
        Method to click on receiver
        :return None
        @param receiver_name: receiver name
        """
        self.look_element(TunesAppLocators.RECEIVER, param=receiver_name).click()

    def click_dongle_pair_headset(self) -> None:
        """
        Method to click dongle pair headset
        :return None
        """
        self.look_element(TunesAppLocators.DONGLE_PAIR_HEADSET).click()

    def click_dongle_pair_continue(self) -> None:
        """
        Method to click continue for dongle to enter pairing mode
        :return None
        """
        self.look_element(TunesAppLocators.DONGLE_CONTINUE_BUTTON).click()

    def click_dongle_pair_done(self) -> None:
        """
        Method to click Done for dongle pairing
        :return None
        """
        self.look_element(TunesAppLocators.DONGLE_PAIR_DONE_BUTTON).click()

    def verify_dock_headset_paired(self) -> bool:
        """
        Method to verify if headset is paired with logi dock
        :return True if unpair button is shown
        """
        return self.verify_element(TunesAppLocators.LOGI_DOCK_UNPAIR_HEADSET)

    def click_more_details(self) -> None:
        """
        Method to click More Details in camera's 'about the device' section.

        Return: None
        """
        self.look_element(TunesAppLocators.MORE_DETAILS).click()

    def close_more_details(self) -> None:
        """
        Method to close More Details in camera's 'about the device' section.

        Return: None
        """
        self.look_element(TunesAppLocators.MORE_DETAILS_CLOSE).click()

    def get_camera_fw_versions_from_more_details(self, elements_to_find: List[str]) -> List[str]:
        """
        Method to get camera's firmware version from More Details View.
        The method is searching for all the elements in provided list.

        Return: List with found elements' versions (or None if element is not found) in order of provided list
        """
        time.sleep(1)
        firmware_versions = []

        for element in elements_to_find:
            found_element = self.look_element_by_text(TunesAppLocators.MORE_DETAILS_TITLE, element)
            if found_element:
                element_parent = found_element.find_element(By.XPATH, '..')
                try:
                    element_version = re.search('[\d\.]+', element_parent.text).group()
                except AttributeError:
                    element_version = None
                Report.logInfo(f'Found {element} version: {element_version}')
            else:
                element_version = None
                Report.logInfo(f'{element} not found in More Details')

            firmware_versions.append(element_version)

        return firmware_versions

    def verify_statusbar_battery(self) -> bool:
        """ Method to verify if statusbar with battery sign is dispalyed for device.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.STATUSBAR_BATTERY)

    def check_battery_level(self, device_name: str) -> int:
        battery_element = self.look_element(TunesAppLocators.BATTERY_LEVEL_FOR_DEVICE, param=device_name,
                                            skip_exception=True)
        return int(battery_element.text.split("%")[0])

    def check_charging_status(self, device_name: str) -> bool:
        is_charging = self.verify_element(TunesAppLocators.DEVICE_IS_CHARGING, param=device_name, timeunit=5)
        return is_charging

    def wait_until_battery_level(self, device_name: str, battery_level: int, timeout: int = 30) -> None:
        charging_start_time = datetime.now()
        while True and (datetime.now() - charging_start_time).seconds < timeout * 60:
            battery_element = self.look_element(TunesAppLocators.BATTERY_LEVEL_FOR_DEVICE, param=device_name)
            current_battery_level = int(battery_element.text.split("%")[0])
            Report.logInfo(f"Current battery level for {device_name} is {current_battery_level}%")
            if current_battery_level >= battery_level:
                Report.logInfo(f"Battery charged to {battery_level} with success")
                return
            time.sleep(30)

    @staticmethod
    def _get_tune_process():
        for proc in psutil.process_iter(['name']):
            if "LogiTune" == proc.info['name'] or "LogiTune.exe" == proc.info['name'] :
                return proc
        return None

    def wait_for_tune_restart(self):
        tune_process = self._get_tune_process()
        if not tune_process:
            Report.logException("Tune Process not found -> Tune is not updating")
            return False
        current_tune_start_time = tune_process.create_time()

        update_start_time = time.time()
        while time.time() - update_start_time < 120:
            updated_tune_proc = self._get_tune_process()
            if updated_tune_proc:
                if updated_tune_proc.create_time() != current_tune_start_time:
                    return True
            time.sleep(5)
        return False

    def verify_anti_startle_label_displayed(self) -> bool:
        """ Method to verify is Anti Starle protection label is displayed on the dashboard.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.DASHBOARD_ANTI_STARTLE_PROTECTION_LABEL)

    def verify_in_ear_detection_label_displayed(self) -> bool:
        """ Method to verify is In-ear detection label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.IN_EAR_DETECTION)

    def verify_enable_receiver_connection_label_displayed(self) -> bool:
        """ Method to verify is Enable Receiver Connection label is displayed.

        @return: True if label is displayed, False otherwise
        """
        return self.verify_element(TunesAppLocators.ENABLE_RECEIVER_CONNECTION)

    def get_in_ear_detection_state(self) -> bool:
        """ Method to get state of the Auto-Pause toggle

        @return: state of the toggle
        """
        element = self.look_element(TunesAppLocators.IN_EAR_DETECTION_CHECKBOX)
        return element.wrapped_element.is_selected()

    def click_in_ear_detection_toggle(self) -> None:
        """ Method to click In-ear detection toggle.

        @return: None
        """
        self.look_element(TunesAppLocators.IN_EAR_DETECTION_TOGGLE).click()

    @staticmethod
    def _check_if_file_contains(path, value):
        with open(path, 'r') as f:
            return value in f.read().splitlines()

    def _verify_if_tf_file_is_valid_(self, path):
        return os.path.exists(path) and \
               self._check_if_file_contains(path, LOCAL_UPDATE_ENABLED_STRING)

    def _create_config_file_if_not_exists(self):

        if 'dar' in sys.platform:
            file_path = os.path.join(r'/Applications', TUNE_FEATURES_FILENAME)
            if not self._verify_if_tf_file_is_valid_(file_path):
                try:
                    with open(file_path, 'w') as file:
                        file.write(LOCAL_UPDATE_ENABLED_STRING)
                    Report.logInfo(f'Config file has been created!')
                except PermissionError as e:
                    Report.logInfo(f'No permissions to create file in directory: {file_path}')
                    raise e
        else:
            file_path = os.path.join(r'C:\Program Files (x86)', TUNE_FEATURES_FILENAME)
            _util_script = os.path.join(DIR_UTILS_PATH, "config_file.bat")
            if not self._verify_if_tf_file_is_valid_(file_path):
                os.system(_util_script)
                Report.logInfo(f'Config file has been created!')

    @staticmethod
    def _delete_config_file_if_exists():

        if 'dar' in sys.platform:
            file_path = os.path.join(r'/Applications', TUNE_FEATURES_FILENAME)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    Report.logInfo(f'Config file has been deleted!')
                except PermissionError as e:
                    Report.logInfo(f'No permissions to remove file in directory: {file_path}')
                    raise e
        else:
            file_path = os.path.join(r'C:\Program Files (x86)', TUNE_FEATURES_FILENAME)
            _del_script = os.path.join(DIR_UTILS_PATH, "delete_file.bat")
            if os.path.exists(file_path):
                try:
                    os.system(_del_script)
                    Report.logInfo(f'Config file has been removed!')
                except PermissionError as e:
                    Report.logInfo(f'No permissions to remove file in directory: {file_path}')
                    raise e
