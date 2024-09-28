import copy
import os
import subprocess
from typing import Any, Dict, Optional, Tuple, Union

import psutil
import requests
import wget
import sys
if not sys.platform.startswith('dar'):
    import winapps
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.common.exceptions import NoSuchWindowException

from apps.tune.TuneAppSettings import TuneAppSettings
from apps.tune.TuneElectron import TuneElectron
from base import global_variables, base_settings
from base.base_ui import UIBase
from base.listener import CustomListener
from pathlib import Path
import time
import pygetwindow as gw

from apps.DriverOpenApp import GetDriverForOpenApp
from apps.win_app_driver_reworked import WinAppDriverAppiumOptions, element_json_to_web_element
from base.base_settings import LOGITUNES_PROD_EP, LOGITUNE_HEADER
from common.aws_s3_utils import AwsS3Utils
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from locators.tunes_ui_locators import TunesInstallerLocators, TunesAppLocators


class TunesUIInstallWindows(UIBase):
    def __init__(self):
        super().__init__()
        self._driver = None
        self._desktop_session = None
        self._report = Report()

    @staticmethod
    def _close_existing_tune_app_installer_exe() -> None:
        app_name_prefix = "LogiTuneInstall"
        for proc in psutil.process_iter(['name']):
            name = proc.info['name']
            if name and name.startswith(app_name_prefix) and name.endswith('.exe'):
                try:
                    proc.terminate()
                    Report.logInfo(f"The process {name} has been terminated.")
                except Exception as e:
                    Report.logInfo(f'Error while killing the process: {e}')

    def install_app(self, version, tune_env: Optional[str] = None,
                    app_update: Optional[str] = None) -> None:

        self._close_existing_tune_app_installer_exe()

        root_path = UIBase.rootPath
        file_path = f'{root_path}\\installers\\LogiTuneInstall{version}.exe'
        app_file = Path(file_path)
        if not app_file.exists():
            valid_version = self._download_app_from_s3(version, root_path)
            version = version if valid_version is None else valid_version
            file_path = f'{root_path}\\installers\\LogiTuneInstall{version}.exe'
        os.startfile(file_path)
        time.sleep(10)

        driver_raw = self._get_driver("Logi Tune Installer")
        if not driver_raw:
            driver_raw = self._get_driver("Logi Tune Install")
        self._driver = EventFiringWebDriver(driver_raw, CustomListener())
        self._report.logInfo("Launching Logi Tune Installer")
        WebDriverWait(self._driver, 30).until(expected_conditions.visibility_of(
            self._look_element(TunesInstallerLocators.WELCOME_INSTALL)))
        self.start_performance_test()
        self._look_element(TunesInstallerLocators.INSTALL).click()
        self._look_element(TunesInstallerLocators.CONFIRM).click()
        i = 100
        while i > 0:
            time.sleep(1)
            try:
                self._get_windows_element_by_name("LogiTune").click()
                break
            except NoSuchElementException:
                i -= 1

        self._report.logPass("Installation complete", True)
        time.sleep(20)
        self._get_windows_element_by_name("Launch Logi Tune").click()

        tunes_app = TuneElectron()
        tunes_app.close_tune_app_windows()

        self.end_performance_test("Logi Tune Installation")
        tune_settings = TuneAppSettings()
        if tune_env or app_update:
            tune_settings.adjust_logitune_settings_file(tune_env=tune_env, app_update=app_update)
        if global_variables.PROXY_PAC is not None:
            pac_file = 'C:/ProgramData/Logitech/Tune/ProxyAutoConfigUrl.txt'
            if os.path.exists(pac_file):
                os.remove(pac_file)
            os.system(
                f"echo {eval(f'global_variables.{global_variables.PROXY_PAC}')} >> {pac_file}"
            )
            tunes_app = TuneElectron()
            tunes_app.close_tune_app_windows()
        time.sleep(5)

    def _look_element(self, element: Tuple[str, str], param: Optional[str] = None,
                      timeout: int = 30, scroll_flag: bool = True, skip_exception: bool = False,
                      wait_for_visibility: bool = False) -> WebElement:
        try:
            element = (element[0], element[1].replace('XXX', param)) if param else element
            if wait_for_visibility:
                WebDriverWait(self._driver, timeout).until(
                    expected_conditions.visibility_of_element_located(element))
            else:
                WebDriverWait(self._driver, timeout).until(
                    expected_conditions.presence_of_element_located(element))
            found_element = self._driver.find_element(*element)
            found_element = element_json_to_web_element(self._driver, found_element)
            try:
                if scroll_flag:
                    self._driver.execute_script("arguments[0].scrollIntoView(false); ",
                                                found_element)
            except Exception as e:
                print(f"Cannot scroll into view - {repr(e)}")
            return found_element

        except Exception as e:
            if not skip_exception:
                self._report.logException(f"Unable to find element- {element}")
                raise e
            else:
                pass

    def uninstall_app(self) -> None:
        self._close_existing_tune_app_installer_exe()

        import subprocess
        if not (os.path.exists(base_settings.TUNES_APP_PATH_WIN)
                or os.path.exists(base_settings.TUNES_APP_PATH_WIN_NEW)):
            self._report.logInfo("Logi Tune not installed")
            return
        try:
            subprocess.run('control')
            time.sleep(2)
            self._report.logInfo("Get driver Control Panel")
            driver_raw = self._get_driver("Control Panel")
            self._driver = EventFiringWebDriver(driver_raw, CustomListener())
            self._report.logInfo("Launching Control Panel")
            try:
                self._look_element(TunesInstallerLocators.UNINSTALL_PROGRAM).click()
                self._look_element(TunesInstallerLocators.UNINSTALL_SEARCH
                                   ).send_keys("tune" + Keys.ENTER)
                time.sleep(2)
                element_logi_tune_icon = self._look_element(TunesInstallerLocators.LOGI_TUNE)
                element_logi_tune_icon.click()
                element_logi_tune_icon.send_keys(Keys.ENTER)
            except WebDriverException as e:
                self._report.logFail(f'Unable to click on Control Panel. Check whether RDP '
                                     f'connection is up and running on main server - {repr(e)}')
            time.sleep(5)
            self._close_control_panel()
            time.sleep(3)
            self._get_windows_element_by_name(TunesInstallerLocators.UNINSTALL_APP[1]).click()
            self.start_performance_test()
            i = 50
            while i > 0:
                time.sleep(2)
                try:
                    self._get_windows_element_by_name(
                        TunesInstallerLocators.UNINSTALL_REBOOT_LATER[1]).click()
                    break
                except NoSuchElementException:
                    i -= 1

            self._report.logPass("Uninstallation complete", True)
            self.end_performance_test("Logi Tune Uninstall")

        except Exception as e:
            print(f'app_uninstall exception: {repr(e)}')
            self._report.logInfo("LogiTune not installed")
        finally:
            self._driver.quit()

    @staticmethod
    def _close_control_panel() -> None:
        control_panel_labels = (
            r'tune - Programs and Features',
            r'tune - Control Panel\Programs\Programs and Features'
        )
        for label in control_panel_labels:
            try:
                window = gw.getWindowsWithTitle(label)[0]
                window.close()
                break
            except IndexError:
                continue

    def _verify_logi_tune_services_installed(self) -> bool:
        import win32serviceutil
        try:
            win32serviceutil.QueryServiceStatus('LogiTuneUpdaterService')
            return True
        except Exception as e:
            self._report.logInfo(repr(e))
            return False

    def verify_logi_tune_services_install(self) -> bool:
        tune_services_installed = self._verify_logi_tune_services_installed()
        if tune_services_installed:
            self._report.logPass("LogiTuneUpdaterService installed")
        else:
            self._report.logFail(f"LogiTuneUpdaterService not installed")
        return tune_services_installed

    def verify_logi_tune_services_uninstall(self) -> bool:
        tune_services_installed = self._verify_logi_tune_services_installed()
        if not tune_services_installed:
            self._report.logPass("LogiTuneUpdaterService removed")
        else:
            self._report.logFail("LogiTuneUpdaterServicee not removed")
        return tune_services_installed

    def download_production_tuneapp(self) -> Optional[str]:
        """
        This method is to download and install latest tuneapp from production
        server.
        :return:
        """
        try:
            self.platform = get_custom_platform()
            req = requests.get(LOGITUNES_PROD_EP,
                               headers=LOGITUNE_HEADER)
            response = req.json()
            _version = response['version']
            self._report.logInfo(f"Latest version of the tuneapp in "
                                 f"production server is {_version}")

            current_directory = os.path.dirname(__file__)
            root_path = Path(current_directory).parent

            tuneapp_msi_url = response["packages"][0]["url"]
            tune_binary = f"{root_path}\\installers\\"
            if not os.path.exists(tune_binary):
                os.makedirs(tune_binary)

            _target = os.path.join(tune_binary, f"LogiTuneInstall{_version}.exe")

            # Delete the target file if exists
            if os.path.exists(_target):
                os.remove(_target)
            self._report.logInfo(f'Please wait till Tune App get downloads')
            wget.download(tuneapp_msi_url, _target)

            return _version
        except Exception as ex:
            self._report.logException("Download of tuneapp failed")
            raise ex

    def check_for_app_installed_win(self, app_name: str) -> Optional[Any]:
        """
        Method to check provided app installed in windows

        :param app_name: str with app name
        :return: 'app obj' or None
        """
        import winapps
        for app in winapps.list_installed():
            if app_name in app.name:
                self._report.logInfo(f"Currently Installed App: {app.name}")
                return app
        return None

    def check_update_app_status(self) -> bool:
        """
        Method to check app update status in windows

        :return: bool
        """
        tune_name = "Logi Tune"
        try:
            self._get_windows_element_by_name(tune_name)
            Report.logInfo(f"Valid Tune name from version 3.7.x is: {tune_name}")
        except Exception as e:
            tune_name = "LogiTune"
            Report.logInfo(f"{repr(e)} - Valid Tune name is: {tune_name}")
        # 1. Wait until LogiTune logo is disappeared on desktop during app updating.
        for _ in range(100):
            time.sleep(1)
            try:
                self._get_windows_element_by_name(tune_name)
                Report.logInfo("LogiTune icon is still on desktop.")

            except Exception as e:
                Report.logInfo(f"LogiTune is uninstalled during updating successfully. - {repr(e)}")
                break

        # 2. Wait until LogiTune logo is shown on desktop during app updating.
        for _ in range(100):
            time.sleep(1)
            try:
                self._get_windows_element_by_name(tune_name).click()
                Report.logInfo("LogiTune icon is on desktop again")
                break

            except Exception as e:
                Report.logInfo(f"LogiTune is not yet shown on desktop during app updating. - "
                               f"{repr(e)}")

        # Wait 20 seconds to let Tune fully up.
        time.sleep(20)
        self._get_windows_element_by_name("OK").click()
        return True

    def get_production_version_tune(self) -> str:
        """
        This method is to get the version of latest tuneapp from production server.

        :return: production_version
        """
        try:
            req = requests.get(LOGITUNES_PROD_EP,
                               headers=LOGITUNE_HEADER)
            response = req.json()
            _version = response['version']
            self._report.logInfo(f"Latest version of the tuneapp "
                                 f"in production server is {_version}")
            return _version

        except Exception as ex:
            self._report.logException("Failed to get current production version")
            raise ex

    def _get_driver(self, app_name: str) -> Optional[WebDriver]:
        try:
            element = self._get_windows_element_by_name(app_name)
            win_handle_hex = f"{int(element.get_attribute('NativeWindowHandle')):x}"

            desired_cap_control_panel = {"appTopLevelWindow": win_handle_hex}
            options_control = WinAppDriverAppiumOptions().load_capabilities(desired_cap_control_panel)
            driver = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                      direct_connection=False, options=options_control)
        except Exception as e:
            print(f'Exception in _get_driver: {repr(e)}')
            return None
        return driver

    def _get_windows_element_by_name(self, element_name: str) -> Optional[WebElement]:
        if self._desktop_session is None:
            desired_cap = {"app": "Root"}
            options_root = WinAppDriverAppiumOptions().load_capabilities(desired_cap)
            self._desktop_session = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                                     direct_connection=False, options=options_root)
        element = self._desktop_session.find_element(By.NAME, element_name)
        element = element_json_to_web_element(self._desktop_session, element)
        return element

    def _download_app_from_s3(self, version: str, root_path: str) -> Optional[str]:
        try:
            path = os.path.join(root_path, "installers")
            file_path = os.path.join(root_path, "installers", f"LogiTuneInstall{version}.exe")
            app_file = Path(file_path)
            if not app_file.exists():
                self._report.logInfo(f"Looking for valid S3 path to Logi Tune {version}")
                aws_utils = AwsS3Utils()
                found_path = aws_utils.find_prefix_with_tune_version(version)
                if found_path is None:
                    raise FileNotFoundError
                self._report.logInfo(f"Found valid path for '{version}' - {found_path}")
                version = found_path.split("/")[2]
                if os.path.isfile(os.path.join(path, f"LogiTuneInstall{version}.exe")):
                    self._report.logInfo("Logi Tune file already downloaded")
                    return version
                prefix = f'vc-sw-release/{found_path}{get_custom_platform()}/LogiTuneInstall.exe'
                aws_utils.download_from_S3(source=prefix, destination=path)

                os.rename(os.path.join(path, "LogiTuneInstall.exe"),
                          os.path.join(path, f"LogiTuneInstall{version}.exe"))
                self._report.logInfo(f"LogiTuneInstall{version}.exe "
                                     f"downloaded to \\installers\\ folder.")
                return version
            else:
                self._report.logInfo("Logi Tune file already downloaded")
        except Exception as e:
            self._report.logException("Not possible to download file from S3.")
            raise e


class TunesUIInstall(UIBase):

    def __init__(self):
        self.desired_cap = {}
        self.report = Report()

    def download_app_from_s3(self, version, root_path) -> Optional[str]:
        try:
            path = os.path.join(root_path, "installers")
            file_path = os.path.join(root_path, "installers", f"LogiTuneInstall{version}.exe")
            app_file = Path(file_path)
            if not app_file.exists():
                self.report.logInfo(f"Looking for valid S3 path to Logi Tune {version}")
                aws_utils = AwsS3Utils()
                found_path = aws_utils.find_prefix_with_tune_version(version)
                if found_path is None:
                    raise FileNotFoundError
                self.report.logInfo(f"Found valid path for '{version}' - {found_path}")
                version = found_path.split("/")[2]
                if os.path.isfile(os.path.join(path, f"LogiTuneInstall{version}.exe")):
                    self.report.logInfo("Logi Tune file already downloaded")
                    return version
                prefix = f'vc-sw-release/{found_path}{get_custom_platform()}/LogiTuneInstall.exe'
                aws_utils.download_from_S3(source=prefix, destination=path)

                os.rename(os.path.join(path, "LogiTuneInstall.exe"),
                          os.path.join(path, f"LogiTuneInstall{version}.exe"))
                self.report.logInfo(f"LogiTuneInstall{version}.exe "
                                    f"downloaded to \\installers\\ folder.")
                return version
            else:
                self.report.logInfo("Logi Tune file already downloaded")
        except Exception as e:
            self.report.logException("Not possible to download file from S3.")
            raise e

    def __getDriver(self, appName):
        desired_cap = {}
        desired_cap["app"] = "Root"
        desktopSession = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                            desired_capabilities=desired_cap)
        app = desktopSession.find_element(By.NAME, appName)
        app.click()
        WinHandle = int(app.get_attribute("NativeWindowHandle"))
        WinHandleHex = f"{WinHandle:x}"
        desired_cap1 = {}
        desired_cap1["appTopLevelWindow"] = WinHandleHex
        driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", desired_capabilities=desired_cap1)
        return driver

    def __get_element_from_desktop(self, element_name):
        desired_cap = {}
        desired_cap["app"] = "Root"
        desktopSession = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                          desired_capabilities=desired_cap)
        element_found = desktopSession.find_element(By.NAME, element_name)
        return element_found

    def installApp(self, version, tune_env: Optional[str] = None, app_update: Optional[str] = None):
        rootPath = UIBase.rootPath
        filePath = f'{rootPath}\\installers\\LogiTuneInstall{version}.exe'
        appFile = Path(filePath)
        if not appFile.exists():
            valid_version = self.download_app_from_s3(version, rootPath)
            version = version if valid_version is None else valid_version
            filePath = f'{rootPath}\\installers\\LogiTuneInstall{version}.exe'

        self.desired_cap["app"] = filePath #destinationFile
        os.startfile(filePath)
        time.sleep(10)
        driverRaw = self.__getDriver("Logi Tune Install")
        self.driver = EventFiringWebDriver(driverRaw, CustomListener())
        self.report.logInfo("Launching Logi Tune Installer")
        self.driver.implicitly_wait(base_settings.IMPLICIT_WAIT)
        self.wait = WebDriverWait(self.driver, base_settings.EXPLICIT_WAIT)
        global_variables.driver = self.driver
        self.wait.until(expected_conditions.visibility_of(self.look_element(TunesInstallerLocators.WELCOME_INSTALL)))
        self.start_performance_test()
        self.look_element(TunesInstallerLocators.INSTALL).click()
        self.look_element(TunesInstallerLocators.CONFIRM).click()
        # Wait until instalation window dissapear
        while True:
            try:
                time.sleep(1)
                self.driver.wrapped_driver.current_window_handle
            except NoSuchWindowException:
                Report.logInfo("Tune Install window closed, continuing...")
                break

        i = 100
        while i > 0:
            time.sleep(1)
            try:
                self.__get_element_from_desktop("LogiTune").click()
                break
            except Exception:
                i -= 1

        self.report.logPass("Installation complete", True)
        time.sleep(20)
        driver = self.__getDriver("LogiTune")
        driver.find_element(By.NAME, "Launch Logi Tune").click()

        self.tunesApp = TuneElectron()
        self.tunesApp.close_tune_app_windows()

        self.end_performance_test("Logi Tune Installation")
        tune_settings = TuneAppSettings()
        if tune_env or app_update:
            tune_settings.adjust_logitune_settings_file(tune_env=tune_env, app_update=app_update)
        if global_variables.PROXY_PAC is not None:
            pac_file = 'C:/ProgramData/Logitech/Tune/ProxyAutoConfigUrl.txt'
            if os.path.exists(pac_file):
                os.remove(pac_file)
            os.system(f"echo {eval(f'global_variables.{global_variables.PROXY_PAC}')} >> {pac_file}")
            self.tunesApp = TuneElectron()
            self.tunesApp.close_tune_app_windows()
        time.sleep(5)

    def uninstallApp(self):
        import win32api
        import win32con
        if not (os.path.exists(base_settings.TUNES_APP_PATH_WIN)
                or os.path.exists(base_settings.TUNES_APP_PATH_WIN_NEW)):
            self.report.logInfo("Logi Tune not installed")
            return
        try:
            win32api.WinExec("control.exe", win32con.SW_NORMAL)
            subprocess.run('control')
            time.sleep(2)
            app = GetDriverForOpenApp()
            self.report.logInfo("Get driver Control Panel")
            driverRaw = app.getDriver("Control Panel")
            self.driver = EventFiringWebDriver(driverRaw, CustomListener())
            global_variables.driver = self.driver
            self.report.logInfo("Launching Control Panel")
            self.look_element(TunesInstallerLocators.UNINSTALL_PROGRAM).click()
            self.look_element(TunesInstallerLocators.UNINSTALL_SEARCH).send_keys("tune"+Keys.ENTER)
            time.sleep(2)
            element = self.look_element(TunesInstallerLocators.LOGI_TUNE)

            actions = ActionChains(global_variables.driver)
            actions.move_to_element(element)
            actions.double_click()
            actions.perform()

            time.sleep(5)
            self.__get_element_from_desktop(TunesInstallerLocators.UNINSTALL_APP[1]).click()
            global_variables.driver.quit()
            self.start_performance_test()
            i = 50
            while i > 0:
                time.sleep(2)
                try:
                    self.__get_element_from_desktop(
                        TunesInstallerLocators.UNINSTALL_REBOOT_LATER[1]).click()
                    break
                except Exception:
                    i -= 1

            self.report.logPass("Uninstallation complete", True)
            self.end_performance_test("Logi Tune Uninstall")
            time.sleep(3)

            try:
                all_windows = gw.getAllWindows()
                for window in all_windows:
                    if "Programs and Features" in window.title or "Control Panel" in window.title:
                        window.close()
            except Exception as e:
                Report.logWarning(e)

        except:
            self.report.logInfo("LogiTune not installed")
            self.driver.quit()

    def verify_logi_tune_services_install(self):
        import win32serviceutil
        flag = True
        try:
            win32serviceutil.QueryServiceStatus('LogiTuneUpdaterService')
            self.report.logPass("LogiTuneUpdaterService installed")
        except:
            self.report.logFail("LogiTuneUpdaterService not installed")
            flag = False


        return flag

    def verify_logi_tune_services_uninstall(self):
        import win32serviceutil
        flag = True

        try:
            win32serviceutil.QueryServiceStatus('LogiTuneUpdaterService')
            self.report.logFail("LogiTuneUpdaterServicee not removed")
            flag = False
        except:
            self.report.logPass("LogiTuneUpdaterService removed")

        return flag


    def download_production_tuneapp(self):
        """
        This method is to download and install latest tuneapp from production
        server.
        :return:
        """
        try:
            self.platform = get_custom_platform()
            req = requests.get(LOGITUNES_PROD_EP,
                               headers=LOGITUNE_HEADER)
            response = req.json()
            _version = response['version']
            self.report.logInfo("Latest version of the tuneapp in production server is {}".format(_version))

            currentDirectory = os.path.dirname(__file__)
            rootPath = Path(currentDirectory).parent

            tuneapp_msi_url = response["packages"][0]["url"]
            tune_binary = str(rootPath) + "\\installers\\"
            if not os.path.exists(tune_binary):
                os.makedirs(tune_binary)

            _target = os.path.join(tune_binary, f"LogiTuneInstall{_version}.exe")

            # Delete the target file if exists
            if os.path.exists(_target):
                os.remove(_target)
            self.report.logInfo(f'Please wait till Tune App get downloads')
            wget.download(tuneapp_msi_url, _target)

            return _version
        except Exception as ex:
            self.report.logException("Download of tuneapp failed")
            raise ex

    def check_for_app_installed_win(self,app_name):
        """
        Method to check provided app installed in windows

        :param app:
        :return: 'app obj' or None
        """
        import winapps
        for app in winapps.list_installed():
            if app_name in app.name:
                self.report.logInfo(f"Currently Installed App: {app.name}")
                return app
        return None

    def check_update_app_status(self) -> bool:
        """
        Method to check app update status in windows

        :return: bool
        """
        # 1. Wait until LogiTune logo is disappeared on desktop during app updating.
        tune_name = "Logi Tune"
        try:
            self.__get_element_from_desktop(tune_name)
            Report.logInfo(f"Valid Tune name from version 3.7.x is: {tune_name}")
        except Exception as e:
            tune_name = "LogiTune"
            Report.logInfo(f"{repr(e)} - Valid Tune name is: {tune_name}")
        for _ in range(100):
            time.sleep(1)
            try:
                self.__get_element_from_desktop(tune_name)
                Report.logInfo("LogiTune icon is still on desktop.")

            except Exception:
                Report.logInfo("LogiTune is uninstalled during updating successfully.")
                break

        # 2. Wait until LogiTune logo is shown on desktop during app updating.
        for _ in range(100):
            time.sleep(1)
            try:
                self.__get_element_from_desktop(tune_name).click()
                Report.logInfo("LogiTune icon is on desktop again")
                break

            except Exception:
                Report.logInfo("LogiTune is not yet shown on desktop during app updating.")

        # Wait 20 seconds to let Tune fully up.
        time.sleep(20)
        driver = self.__getDriver(tune_name)
        driver.find_element(By.NAME, "OK").click()
        driver.quit()
        return True

    def get_production_version_tune(self) -> str:
        """
        This method is to get the version of latest tuneapp from production server.

        :return: production_version
        """
        try:
            req = requests.get(LOGITUNES_PROD_EP,
                               headers=LOGITUNE_HEADER)
            response = req.json()
            _version = response['version']
            self.report.logInfo(f"Latest version of the tuneapp in production server is {_version}")
            return _version

        except Exception as ex:
            self.report.logException("Failed to get current production version")
            raise ex
