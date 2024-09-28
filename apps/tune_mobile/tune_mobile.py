import os

from appium.options.android import UiAutomator2Options
from apps.tune_mobile.tune_mobile_testflight import TuneMobileTestFlight
from common.aws_s3_utils import AwsS3Utils
from pathlib import Path
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from apps.tune_mobile.config import tune_mobile_config
from base import global_variables
from base.base_mobile import MobileBase
from base.base_ui import UIBase
from base.listener import CustomListener
from extentreport.report import Report
from appium import webdriver


class TuneMobile(MobileBase):
    # index = MobileBase.index

    def open(self, teammate : bool = False):
        """
        Method to open Tune Mobile app

        :param :
        :return :
        """
        MobileBase.device = tune_mobile_config.teammate_phone if teammate else tune_mobile_config.phone
        self.desired_caps = {}
        self.desired_caps['platformName'] = self.get_platform_name()
        self.desired_caps['deviceName'] = MobileBase.device
        self.desired_caps['platformVersion'] = self.get_platform_version()
        self.desired_caps['newCommandTimeout'] = tune_mobile_config.new_command_timeout
        if self.is_ios_device():
            self.desired_caps['udid'] = self.get_udid()
            self.desired_caps['bundleId'] = tune_mobile_config.app_package
        else:
            self.desired_caps['appPackage'] = tune_mobile_config.app_package
            self.desired_caps['appActivity'] = tune_mobile_config.app_activity
            self.desired_caps['noReset'] = True
            self.desired_caps['newCommandTimeout'] = 0
            self.desired_caps['keep_alive'] = True
            self.desired_caps['ignoreHiddenApiPolicyError'] = True
            self.desired_caps['automationName'] = tune_mobile_config.android_automationName
        if self.is_android_device():
            self.desired_caps['language'] = tune_mobile_config.locale
            self.desired_caps['locale'] = tune_mobile_config.locale
        Report.logInfo("Launching Tune Mobile App")
        options = UiAutomator2Options().load_capabilities(self.desired_caps)
        driverRaw = webdriver.Remote(f'http://localhost:4753', options=options)
        #Unlock Phone if it is locked (Only for Android)
        if MobileBase.device == "OnePlus":
            driverRaw.update_settings({"waitForIdleTimeout": 0})
        global_variables.driver = driverRaw
        from apps.tune_mobile.phone_settings import PhoneSettings
        phone_settings = PhoneSettings()
        if not phone_settings.unlock_phone():
            driverRaw = webdriver.Remote(f'http://localhost:4753', options=options)

        driverRaw.implicitly_wait(tune_mobile_config.implicit_wait)
        MobileBase.driver = driverRaw
        driver = EventFiringWebDriver(driverRaw, CustomListener())
        global_variables.driver = driver
        return global_variables.driver

    def close(self):
        """
        Method to close Tune Mobile App

        :param :
        :return :
        """
        if global_variables.driver is not None:
            global_variables.driver.quit()
        global_variables.driver = None

    def install_app(self, version: str):
        """
        Method to install Logi Tune Mobile app

        :param version:
        :return :
        """
        if self.is_android_device():
            self.install_app_android(version=version)
        else:
            self.install_app_ios(version=version)

    def install_app_android(self, version: str):
        """
        Method to install Logi Tune Mobile app on Android device

        :param version:
        :return :
        """
        self.download_app_from_s3(version=version, root_path=UIBase.rootPath)
        self.desired_caps = {}
        self.desired_caps['platformName'] = self.get_platform_name()
        self.desired_caps['deviceName'] = MobileBase.device
        self.desired_caps['platformVersion'] = self.get_platform_version()
        if self.is_ios_device():
            self.desired_caps['udid'] = self.get_udid()
            self.desired_caps['bundleId'] = tune_mobile_config.app_package
            self.desired_caps['app'] = f"{UIBase.rootPath}/installers/app_{version}.ipa"
        else:
            self.desired_caps['appPackage'] = tune_mobile_config.app_package
            self.desired_caps['appActivity'] = tune_mobile_config.app_activity
            self.desired_caps['app'] = f"{UIBase.rootPath}/installers/app_{version}.apk"
            self.desired_caps['newCommandTimeout'] = tune_mobile_config.new_command_timeout
            self.desired_caps['ignoreHiddenApiPolicyError'] = True

        Report.logInfo(f"Installing Tune Mobile App {version}")
        driverRaw = webdriver.Remote(f'http://127.0.0.1:{tune_mobile_config.port}/wd/hub', self.desired_caps)
        if tune_mobile_config.phone == "OnePlus":
            driverRaw.update_settings({"waitForIdleTimeout": 0})
        from apps.tune_mobile.tune_mobile_settings import TuneMobileSettings
        driver = EventFiringWebDriver(driverRaw, CustomListener())
        global_variables.driver = driver
        settings = TuneMobileSettings()
        if settings.verify_grant_permission():
            settings.click_grant_permission().click_allow()

    def install_app_ios(self, version: str):
        """
        Method to install Logi Tune Mobile app on iOS device

        :param version:
        :return :
        """
        testflight = TuneMobileTestFlight()
        testflight.install_app(version=version)
        from apps.tune_mobile.tune_mobile_settings import TuneMobileSettings
        settings = TuneMobileSettings()
        self.open()
        notification_count = 0
        for _ in range(4):
            if settings.verify_allow():
                settings.click_allow()
                notification_count += 1
            if settings.verify_ok():
                settings.click_ok()
                notification_count += 1
            if notification_count == 2:
                break
        # if settings.verify_ok(timeout=5):
        #     settings.click_ok()
        #     if settings.verify_allow():
        #         settings.click_allow()
        # elif settings.verify_allow():
        #     settings.click_allow()
        #     if settings.verify_ok():
        #         settings.click_ok()
        settings.click_next().click_start_testing()

    def uninstall_app(self):
        """
        Method to uninstall Logi Tune Mobile app on Android device

        :param :
        :return :
        """
        try:
            driver = self.open()
            Report.logInfo("Uninstalling Tune Mobile App")
            driver.remove_app(tune_mobile_config.app_package)
        except Exception as e:
            Report.logInfo("Tune Mobile App is not installed")
        self.close()

    def update_app(self, version: str):
        """
        Method to install Logi Tune Mobile app

        :param version:
        :return :
        """
        if self.is_android_device():
            self.update_app_android(version=version)
        else:
            self.update_app_ios()

    def update_app_android(self, version: str):
        """
        Method to Update Logi Tune Mobile app on Android device

        :param version:
        :return :
        """
        self.download_app_from_s3(version=version, root_path=UIBase.rootPath)
        try:
            driver = self.open()
            Report.logInfo(f"Updating Tune Mobile App to {version}")
            driver.install_app(f"{UIBase.rootPath}/installers/app_{version}.apk")
        except Exception as e:
            Report.logInfo("Tune Mobile App is not installed or higher version installed")
        self.close()

    def update_app_ios(self):
        """
        Method to Update Logi Tune Mobile app on iOS device

        :param version:
        :return :
        """
        testflight = TuneMobileTestFlight()
        testflight.update_app()
        from apps.tune_mobile.tune_mobile_settings import TuneMobileSettings
        settings = TuneMobileSettings()
        self.open()
        settings.click_next().click_start_testing()

    def download_app_from_s3(self, version, root_path):
        try:
            ext = "ipa" if self.is_ios_device() else "apk"
            file = "Tune" if self.is_ios_device() else "app-prod-release"
            path = os.path.join(root_path, "installers")
            file_path = os.path.join(root_path, "installers", f"app_{version}.{ext}")
            app_file = Path(file_path)
            if not app_file.exists():
                Report.logInfo(f"Looking for valid S3 path to Tune Mobile {version}")
                aws_utils = AwsS3Utils()
                found_path = aws_utils.find_prefix_with_valid_tune_mobile_version(version)
                if found_path is None:
                    raise FileNotFoundError
                prefix = f'vc-sw-release/{found_path}release/{file}.{ext}'
                aws_utils.download_from_S3(source=prefix, destination=path)

                os.rename(os.path.join(path, f"{file}.{ext}"),
                          os.path.join(path, f"app_{version}.{ext}"))
                Report.logInfo(f"app_{version}.apk downloaded to \\installers\\ folder.")
            else:
                Report.logInfo("Tune Mobile App already downloaded")
        except Exception as e:
            Report.logException("Not possible to download file from S3.")
            raise e