import os
import subprocess

import psutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.events import EventFiringWebDriver

from apps.DriverOpenApp import GetDriverForOpenApp
from apps.browser_methods import BrowserClass
from base import base_settings
from base.base_ui import UIBase
from base.listener import CustomListener, CustomBrowserListener
from base.base_settings import IMPLICIT_WAIT
from common.platform_helper import get_custom_platform
from locators.google_meet_locators import GoogleMeetLocators
from locators.win_ui_locators import *
from common.usb_switch import *
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from selenium.webdriver import DesiredCapabilities, ActionChains


class GoogleMeet(UIBase):
    base_driver = None

    def __init__(self):
        pass

    def create_new_meeting(self) -> None:
        """
        Method to create new Google Meet meeting

        :param none
        :return none
        """
        i = 0
        meet_flag = False
        while i < 2:
            i += 1
            try:
                browser = BrowserClass()
                browser.prepare_opened_browser()
                driverRaw = browser.connect_to_current_browser_page()
                global_variables.driver = EventFiringWebDriver(driverRaw, CustomBrowserListener())
                global_variables.driver.maximize_window()
                global_variables.driver.get("https://meet.google.com")
                if self.verify_element(GoogleMeetLocators.TRY_GOOGLE_MEET_WEBAPP_MSG, timeunit=5):
                    self.look_element(GoogleMeetLocators.CLOSE).click()
                self.look_element(GoogleMeetLocators.NEW_MEETING).click()
                self.look_element(GoogleMeetLocators.START_AN_INSTANT_MEETING).click()
                if self.verify_element(GoogleMeetLocators.LEAVE_CALL):
                    meet_flag = True
                    if self.verify_element(GoogleMeetLocators.MEETING_READY):
                        self.look_element(GoogleMeetLocators.MEETING_READY_CLOSE).click()
                    break
                else:
                    Report.logInfo(f"Exception in creating new meeting - Retry {i}")
            except Exception as e:
                Report.logInfo(str(e))
        if meet_flag:
            Report.logInfo("New Google Meet meeting started")
        else:
            Report.logFail("Exception in creating new Google Meet after 3 tries")
            assert False

    def leave_meeting(self) -> None:
        """
        Method to leave Google Meet meeting

        :param none
        :return none
        """
        self.look_element(GoogleMeetLocators.LEAVE_CALL).click()
        if self.verify_element(GoogleMeetLocators.RETURN_TO_HOME, timeunit=10):
            self.look_element(GoogleMeetLocators.RETURN_TO_HOME).click()
        global_variables.driver.close()

    def capture_video_stream(self, name=None):
        """
        Method to capture a screenshot of the video stream and name it.

        :name : filename
        :return none
        """
        element = self.look_element(GoogleMeetLocators.VIDEO_STREAM)
        i = 10
        while i > 0:
            if str(element.get_attribute("style")).__contains__("none"):
                time.sleep(1)
            i -= 1
        time.sleep(5) #Wait for 5 seconds if rightsight moves the lens
        return Report.get_element_screenshot(element, name)
