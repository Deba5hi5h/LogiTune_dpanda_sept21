import os
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

from locators.tune_mobile.tune_mobile_testflight_locators import TuneMobileTestFlightLocators


class TuneMobileTestFlight(MobileBase):

    def open(self):
        """
        Method to open TestFlight app

        :param :
        :return :
        """
        self.desired_caps = {}
        self.desired_caps['platformName'] = self.get_platform_name()
        self.desired_caps['deviceName'] = MobileBase.device
        self.desired_caps['platformVersion'] = self.get_platform_version()
        self.desired_caps['newCommandTimeout'] = tune_mobile_config.new_command_timeout
        self.desired_caps['udid'] = self.get_udid()
        self.desired_caps['bundleId'] = "com.apple.TestFlight"

        Report.logInfo("Launching TestFlight App")
        driverRaw = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        driverRaw.implicitly_wait(tune_mobile_config.implicit_wait)
        MobileBase.driver = driverRaw
        driver = EventFiringWebDriver(driverRaw, CustomListener())
        global_variables.driver = driver
        if self.verify_continue():
            self.click_continue()
        return global_variables.driver

    def close(self):
        """
        Method to close TestFlight App

        :param :
        :return :
        """
        if global_variables.driver is not None:
            global_variables.driver.quit()
        global_variables.driver = None

    def click_logitune(self):
        """
        Method to click Logi Tune

        :param :
        :return TuneMobileTestFlight:
        """
        self.find_element(TuneMobileTestFlightLocators.LOGITUNE, visibility=False).click()
        return self

    def click_previous_builds(self):
        """
        Method to click Previous Builds

        :param :
        :return TuneMobileTestFlight:
        """
        self.find_element(TuneMobileTestFlightLocators.PREVIOUS_BUILDS).click()
        return self

    def click_version(self, version: str):
        """
        Method to click Major version

        :param version:
        :return TuneMobileTestFlight:
        """
        major_version = version.split('-')[0].strip()
        self.find_element(TuneMobileTestFlightLocators.VERSION, param=major_version).click()
        return self

    def click_install(self, version: str):
        """
        Method to click Install button

        :param version:
        :return TuneMobileTestFlight:
        """
        major_version = version.split('-')[0].strip()
        minor_version = version.split('-')[1].strip()
        version = f"{major_version} ({minor_version})"
        self.find_element(TuneMobileTestFlightLocators.INSTALL, param=version).click()
        return self

    def click_confirm_install(self):
        """
        Method to click Install button on confirmation popup

        :param :
        :return TuneMobileTestFlight:
        """
        self.find_element(TuneMobileTestFlightLocators.CONFIRM_INSTALL).click()
        return self

    def verify_confirm_install(self):
        """
        Method to verify Install button on confirmation popup

        :param :
        :return TuneMobileTestFlight:
        """
        self.verify_element(TuneMobileTestFlightLocators.CONFIRM_INSTALL, timeout=2)
        return self

    def click_update(self):
        """
        Method to click Update button

        :param :
        :return TuneMobileTestFlight:
        """
        self.find_element(TuneMobileTestFlightLocators.UPDATE, visibility=False).click()
        return self

    def click_continue(self):
        """
        Method to click Continue button

        :param :
        :return TuneMobileTestFlight:
        """
        self.find_element(TuneMobileTestFlightLocators.CONTINUE).click()
        return self

    def verify_continue(self) -> bool:
        """
        Method to verify Continue button displayed

        :param version:
        :return bool:
        """
        return self.verify_element(TuneMobileTestFlightLocators.CONTINUE, timeout=2)

    def verify_open_button(self) -> bool:
        """
        Method to verify OPEN button displayed

        :param version:
        :return bool:
        """
        return self.verify_element(TuneMobileTestFlightLocators.OPEN, timeout=60)

    def install_app(self, version: str):
        """
        Method to install Tune Mobile app from TestFlight

        :param version:
        :return :
        """
        self.open()
        self.click_logitune().click_previous_builds().click_version(version=version).click_install(version=version)
        #Below code needs to be uncommented when the pop-up starts appearing again by updating locator
        # if self.verify_install_popup():
        #     self.click_popup_install()
        if self.verify_open_button():
            Report.logInfo(f"Successfully installed Logi Tune {version}")

    def update_app(self):
        """
        Method to Update Tune Mobile app from TestFlight

        :param :
        :return :
        """
        self.open()
        self.click_update()
        if self.verify_open_button():
            Report.logInfo(f"Successfully updated Logi Tune App")

    def verify_install_popup(self) -> bool:
        """
        Method to verify pop up message displayed with Install button

        :param version:
        :return bool:
        """
        return self.verify_element(TuneMobileTestFlightLocators.INSTALL_POPUP, timeout=5)

    def click_popup_install(self):
        """
        Method to click Install button from the pop up message

        :param :
        :return TuneMobileTestFlight:
        """

        self.find_element(TuneMobileTestFlightLocators.INSTALL_POPUP).click()
        return self