import os
import shutil
import subprocess

import psutil
from appium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.events import EventFiringWebDriver

from apis.sync_helper import SyncHelper
from apps.sync.sync_app import SyncApp
from apps.sync.sync_app_methods import SyncAppMethods
from base import global_variables, base_settings
from base.base_ui import UIBase
from base.listener import CustomListener
from pathlib import Path
import time

from apps.DriverOpenApp import GetDriverForOpenApp
from base.base_settings import IMPLICIT_WAIT, EXPLICIT_WAIT
from common.aws_s3_utils import AwsS3Utils
from common.framework_params import INSTALLER, SYNC_PROD_VERSION1
from common.json_helper import JsonHelper
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from locators.win_ui_locators import *


class AppInstall(UIBase):
    sync_app = SyncAppMethods()

    def __init__(self):
        self.desired_cap = {}
        self.report = Report()

    def installApp(self, version=None):
        self._clean_up_sync_installation()
        rootPath = UIBase.rootPath  # Path(Path(currentDirectory).parent).parent
        path = str(rootPath) + "\\installers\\"

        if version == None:
            version = INSTALLER
        filePath = os.path.join(rootPath, f"installers/LogiSyncApp-Setup{version}.exe")
        appFile = Path(filePath)
        if not appFile.exists():
            self.download_sync_from_s3(version=version)

        self.desired_cap["app"] = filePath  # destinationFile

        driverRaw = webdriver.Remote(command_executor="http://127.0.0.1:4723", desired_capabilities=self.desired_cap)
        self.driver = EventFiringWebDriver(driverRaw, CustomListener())
        self.report.logInfo(f"Launching Installer {version}")
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        global_variables.driver = self.driver

        self._windows_installer()

        sync_config = 'C:/ProgramData/Logitech/LogiSync/sync-config.json'
        shutil.copy(str(rootPath) + '/installers/sync-config.json', sync_config)
        JsonHelper.update_json(sync_config, 'futen,current', global_variables.SYNC_FUTEN)
        JsonHelper.update_json(sync_config, 'raiden,current', global_variables.SYNC_ENV)
        JsonHelper.update_json(sync_config, 'futen-fwota,current', global_variables.SYNC_FWOTA)
        if global_variables.PROXY_PAC is not None:
            pac_file = 'C:/ProgramData/Logitech/LogiSync/ProxyAutoConfigUrl.txt'
            if os.path.exists(pac_file):
                os.remove(pac_file)
            os.system(f"echo {eval(f'global_variables.{global_variables.PROXY_PAC}')} >> {pac_file}")
        time.sleep(10)
        try:
            for proc in psutil.process_iter():
                if 'Sync.exe' in proc.name():
                    print(f'Killing {proc.name()}')
                    proc.kill()
        except:
            pass
        SyncApp.restart_sync_services()

    def _windows_installer(self):
        self.wait = WebDriverWait(global_variables.driver, EXPLICIT_WAIT)
        self.wait.until(expected_conditions.visibility_of(self.look_element(InstallerLocators.CANCEL)))
        self.start_performance_test()
        self.look_element(InstallerLocators.ACCEPT_TERMS).click()
        self.look_element(InstallerLocators.INSTALL).click()
        i = 600
        while i > 0:
            time.sleep(1)
            if self.verify_element(InstallerLocators.FINISH, 2):
                break
            else:
                i = i - 1
        if self.verify_element(InstallerLocators.REBOOT_LATER, 8):
            self.look_element(InstallerLocators.REBOOT_LATER).click()
        self.report.logPass("Installation complete", True)
        self.look_element(InstallerLocators.FINISH).click()
        self.end_performance_test("Sync App Installation")

    def uninstallApp(self):
        if not os.path.exists(base_settings.SYNC_APP_PATH_WIN):
            Report.logInfo("Sync App not installed")
            self._clean_up_sync_installation()
            return
        try:
            os.system('C:\\"Program Files (x86)"\\Logitech\\LogiSync\\uninst-main.exe')
            time.sleep(10)
            app = GetDriverForOpenApp()
            driverRaw = app.getDriver("LogiSync Uninstall ")
            self.driver = EventFiringWebDriver(driverRaw, CustomListener())
            global_variables.driver = self.driver
            self.look_element(InstallerLocators.UNINSTALL).click()
            self.start_performance_test()
            i = 600
            while i > 0:
                time.sleep(1)
                if self.verify_element(InstallerLocators.FINISH, 2):
                    break
                else:
                    i = i - 1
            if self.verify_element(InstallerLocators.REBOOT_LATER, 2):
                self.look_element(InstallerLocators.REBOOT_LATER).click()
            self.report.logPass("Unnstallation complete", True)
            self.end_performance_test("Sync App Uninstall")
            self.look_element(InstallerLocators.FINISH).click()
            if self.verify_element(InstallerLocators.FINISH, 2):
                self.look_element(InstallerLocators.FINISH).click()
            self._clean_up_sync_installation()
        except Exception as e:
            Report.logException(str(e))
            self.driver.quit()

    @staticmethod
    def _clean_up_sync_installation():

        process = subprocess.run(
            str(UIBase.rootPath) + "\\WinApp\\cleanup_sync.bat",
            shell=True)
        time.sleep(5)  # Wait for file to be created
        for _ in range(600):
            flag = False
            file1 = open(str(UIBase.rootPath) + "\\WinApp\\tmp_read.txt", "r")
            for line in file1:
                # check finish is present in line or not
                if "finish" in line:
                    flag = True
            if flag:
                file1.close()
                break
            time.sleep(1)

    def verify_sync_services_install(self):
        import win32serviceutil
        flag = True
        try:
            win32serviceutil.QueryServiceStatus('LogiSyncHandler Service')
            self.report.logPass("LogiSyncHandler Service installed")
        except:
            self.report.logFail("LogiSyncHandler Service not installed")
            flag = False
        try:
            win32serviceutil.QueryServiceStatus('LogiSyncMiddleware Service')
            self.report.logPass("LogiSyncMiddleware Service installed")
        except:
            self.report.logFail("LogiSyncMiddleware Service not installed")
            flag = False
        try:
            win32serviceutil.QueryServiceStatus('LogiSyncProxy Service')
            self.report.logPass("LogiSyncProxy Service installed")
        except:
            self.report.logFail("LogiSyncProxy Service not installed")
            flag = False
        return flag

    def verify_sync_services_uninstall(self):
        import win32serviceutil
        flag = True
        try:
            win32serviceutil.QueryServiceStatus('LogiSyncMiddleware Service')
            self.report.logFail("LogiSyncMiddleware Service not removed")
            flag = False
        except:
            self.report.logPass("LogiSyncMiddleware Service removed")

        try:
            win32serviceutil.QueryServiceStatus('LogiSyncProxy Service')
            self.report.logFail("LogiSyncProxy Service not removed")
            flag = False
        except:
            self.report.logPass("LogiSyncProxy Service removed")
        return flag

    def verify_registry_install(self):
        from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey
        flag = True
        syncAgent = r'SOFTWARE\Logitech\LogiSyncAgent'
        syncHandler = r'SOFTWARE\Logitech\LogiSyncHandler'
        syncMiddleware = r'SOFTWARE\Logitech\LogiSyncMiddleware'
        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            k = OpenKey(reg, syncAgent)
            self.report.logPass("LogiSyncAgent Registry Key created")
        except:
            self.report.logFail("LogiSyncAgent Registry Key not created")
            flag = False
        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            k = OpenKey(reg, syncHandler)
            self.report.logPass("LogiSyncHandler Registry Key created")
        except:
            self.report.logFail("LogiSyncHandler Registry Key not created")
            flag = False
        return flag

    def verify_registry_uninstall(self):
        from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey
        flag = True
        syncAgent = r'SOFTWARE\Logitech\LogiSyncAgent'
        syncHandler = r'SOFTWARE\Logitech\LogiSyncHandler'
        syncMiddleware = r'SOFTWARE\Logitech\LogiSyncMiddleware'
        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            k = OpenKey(reg, syncAgent)
            self.report.logFail("LogiSyncAgent Registry Key not removed")
            flag = False
        except:
            self.report.logPass("LogiSyncAgent Registry Key removed")

        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            k = OpenKey(reg, syncHandler)
            self.report.logFail("LogiSyncHandler Registry Key not removed")
            flag = False
        except:
            self.report.logPass("LogiSyncHandler Registry Key removed")

        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            k = OpenKey(reg, syncMiddleware)
            self.report.logFail("LogiSyncMiddleware Registry Key not removed")
            flag = False
        except:
            self.report.logPass("LogiSyncMiddleware Registry Key removed")

        return flag

    def download_sync_from_s3(self, version):
        try:
            rootPath = UIBase.rootPath
            path = os.path.join(rootPath, "installers")
            download_folder = ""
            if get_custom_platform() == "windows":
                sync_installer = "LogiSyncApp-Setup"
                sync_ext = ".exe"
                sync_folder = "Windows"
            else:
                sync_installer = "LogiSyncInstaller"
                sync_ext = ".pkg"
                sync_folder = "MAC"
            filePath = os.path.join(rootPath, "installers", f"{sync_installer}{version}{sync_ext}")
            appFile = Path(filePath)
            if not appFile.exists():
                self.report.logInfo(f"Start downloading Sync app {version} from S3")
                branches = ['master', 'rel-2.5-maintenance', 'rel-3.4-kongnr', 'rel-3.5-special']
                for branch in branches:
                    prefix = f'vc-sw-release/OneApp_MVP/{branch}/OneApp_Release/{version}/{sync_folder}/'
                    download_folder = f"OneApp_MVP/{branch}/OneApp_Release/{version}/{sync_folder}/"
                    awsutils = AwsS3Utils()
                    if awsutils.download_from_S3(f'{prefix}{sync_installer}{sync_ext}', destination=path):
                        break
                if os.path.exists(os.path.join(path, download_folder)):
                    os.rename(os.path.join(path, f"{download_folder}{sync_installer}{sync_ext}"),
                              os.path.join(path, f"{sync_installer}{version}{sync_ext}"))
                else:
                    os.rename(os.path.join(path, f"{sync_installer}{sync_ext}"),
                              os.path.join(path, f"{sync_installer}{version}{sync_ext}"))
                self.report.logInfo(f"{sync_installer}{version}{sync_ext} downloaded to \installers\ folder.")
                # if get_custom_platform() == "windows":
                if os.path.exists(os.path.join(path, download_folder)):
                    download_directory = os.path.join(path, "OneApp_MVP")
                    shutil.rmtree(download_directory, ignore_errors=True)
            else:
                self.report.logInfo("Sync App file already downloaded")
        except Exception as e:
            self.report.logException("Not possible to download file from S3.")
            raise e

    def install_sync_mac(self, version):
        currentDirectory = os.path.dirname(__file__)
        rootPath = UIBase.rootPath

        filePath = os.path.join(rootPath, "installers", f"LogiSyncInstaller{version}.pkg")
        appFile = Path(filePath)
        if not appFile.exists():
            self.download_sync_from_s3(version)

        self.report.logInfo("Installing Sync...")
        res = subprocess.check_output(f"sudo installer -pkg {filePath} -target /", shell=True)
        assert "installer: The upgrade was successful." in res.decode(
            'utf-8') or "installer: The install was successful." in res.decode('utf-8'), "AAAAAAAA"

        time.sleep(30)
        os.system('pkill Sync')
        if not os.path.exists('/Users/Shared/LogiSync'):
            os.system('open /Applications/Sync.app')
            time.sleep(30)
            os.system('pkill Sync')
        sync_config = '/Users/Shared/LogiSync/sync-config.json'
        shutil.copy(str(rootPath) + '/installers/sync-config.json', sync_config)
        JsonHelper.update_json(sync_config, 'futen,current', global_variables.SYNC_FUTEN)
        JsonHelper.update_json(sync_config, 'raiden,current', global_variables.SYNC_ENV)
        JsonHelper.update_json(sync_config, 'futen-fwota,current', global_variables.SYNC_FWOTA)

    def uninstall_sync_mac(self):
        if self.check_for_app_installed_macos("Sync") is not True:
            self.report.logInfo("Sync not installed")
            return
        self.report.logInfo("Unistalling Sync...")
        cmd = f"sudo installer -target / -dumplog -pkg /Library/Application\ Support/Logitech/LogiSync/Helpers/Sync_Uninstaller.pkg"
        res = subprocess.check_output(f"{cmd}", shell=True)
        assert "installer: The upgrade was successful." in res.decode(
            'utf-8') or "installer: The install was successful." in res.decode('utf-8'), "AAAAAAAA"
        assert self.check_for_app_installed_macos("Sync") is not True, "Sync uninstalling failed"
        self.report.logPass("Sync Uninstalled successfully")

    @staticmethod
    def check_for_app_installed_macos(app_name: str) -> bool:
        res = subprocess.check_output("system_profiler SPApplicationsDataType", shell=True)
        apps = res.decode("utf-8")
        return f"/Applications/{app_name}.app" in apps

    def update_sync_from_room(self):
        verification = self.sync_app.open().click_room().verify_new_sync_version_available_banner()
        self.sync_app.report_displayed_or_not("New Sync App version available banner", verification)
        self.sync_app.room.click_update()
        self._sync_update_flow()


    def update_sync_from_menu(self):
        try:
            sync_version = SyncHelper.get_logisync_version()
            version_list = sync_version.split('.')
            sync_version = int(version_list[len(version_list)-1])
        except Exception as e:
            sync_version = 0
        self.sync_app.open().click_room()
        self.sync_app.home.click_menu()
        self.sync_app.home.click_updates_and_about().click_check_for_update().click_sync_update_now()
        Report.logInfo("New Sync version available", True)
        self._sync_update_flow()

    def _sync_update_flow(self):
        self.sync_app.home.click_sync_update_now()
        if get_custom_platform() == "windows":
            installer_wait_flag = True
            installer_wait_count = 300
            self.start_performance_test()
            while installer_wait_flag and installer_wait_count > 0:
                for proc in psutil.process_iter():
                    if 'LogiSyncApp' in proc.name():
                        installer_wait_flag = False
                        time.sleep(5)
                        break
                time.sleep(1)
                installer_wait_count -= 1
            self.end_performance_test("Sync App Update")
            app = GetDriverForOpenApp()
            driverRaw = app.getDriver('LogiSync App Installer ')
            self.driver = EventFiringWebDriver(driverRaw, CustomListener())
            self.driver.implicitly_wait(2)
            global_variables.driver = self.driver
            self._windows_installer()
            time.sleep(10)
            try:
                for proc in psutil.process_iter():
                    if 'Sync.exe' in proc.name():
                        print(f'Killing {proc.name()}')
                        proc.kill()
            except Exception as e:
                pass
        else:
            time.sleep(20)
