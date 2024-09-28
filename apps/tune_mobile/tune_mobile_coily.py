from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from apps.tune_mobile.config import tune_mobile_config
from base import global_variables
from base.base_coily import CoilyBase
from base.base_mobile import MobileBase
from base.listener import CustomListener
from extentreport.report import Report
from appium import webdriver

from locators.tune_mobile.tune_mobile_home_locators import TuneMobileHomeLocators


class TuneMobileCoily(CoilyBase):

    def __init__(self):
        self.desired_caps = {}
        self.desired_caps['platformName'] = tune_mobile_config.coily_platform_name
        self.desired_caps['platformVersion'] = tune_mobile_config.coily_platform_version
        self.desired_caps['appPackage'] = tune_mobile_config.coily_app_package
        self.desired_caps['appActivity'] = tune_mobile_config.coily_app_activity
        self.desired_caps['noReset'] = True
        self.desired_caps['newCommandTimeout'] = 0
        self.desired_caps['keep_alive'] = True

    def open_coily(self):
        """
        Method to open Coily Scheduler app

        :param :
        :return :
        """
        Report.logInfo("Launching Coily Scheduler App")
        driverRaw = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        driverRaw.implicitly_wait(tune_mobile_config.implicit_wait)
        CoilyBase.coily_driver = driverRaw
        driver = EventFiringWebDriver(driverRaw, CustomListener())
        global_variables.collabos_driver = driver
        return global_variables.collabos_driver

    def close_coily(self):
        """
        Method to close Coily Scheduler App

        :param :
        :return :
        """
        if global_variables.collabos_driver is not None:
            global_variables.collabos_driver.quit()
        global_variables.collabos_driver = None
