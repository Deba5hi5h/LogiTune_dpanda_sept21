import os
import subprocess
import sys
import time
from typing import Optional

import psutil
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from apps.tune.helpers import get_python_version
from base import global_variables, base_settings
from base.base_ui import UIBase
from base.listener import CustomBrowserListener

from common.platform_helper import get_custom_platform
from extentreport.report import Report


class BrowserClass(UIBase):

    @staticmethod
    def _initialize_chrome_driver(options: Optional[ChromeOptions] = None) -> WebDriver:
        if options is None:
            options = ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9229")
        if get_python_version() < 312:
            return webdriver.Chrome(ChromeDriverManager().install(), options=options)
        else:
            from selenium.webdriver import ChromeService
            service = ChromeService(executable_path=ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _initialize_firefox_driver() -> WebDriver:
        if get_python_version() < 312:
            return webdriver.Firefox(executable_path=GeckoDriverManager().install())
        else:
            from selenium.webdriver import FirefoxService
            service = FirefoxService(executable_path=GeckoDriverManager().install())
            return webdriver.Firefox(service=service)

    def open_browser(self, url, browser=None):
        """
        Method to launch Browser (default browser set in base_settings.py) and navigate to url
        :param url,
        :param browser (optional)
        :return none
        """
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-search-engine-choice-screen')
        if browser is None:
            browser = base_settings.BROWSER
        if browser == "iexplorer":
            # Set ie driver
            self.driverRaw = webdriver.Ie()
        elif browser == "firefox":
            self.driverRaw = self._initialize_firefox_driver()
        elif browser == "chrome":
            # Set chrome driver
            try:
                self.driverRaw = self._initialize_chrome_driver(options=options)
            except WebDriverException as e:
                Report.logWarning("Chrome Crashed to start, relaunching in 10 seconds")
                time.sleep(10)
                self.driverRaw = self._initialize_chrome_driver(options=options)
            except Exception as e:
                Report.logException(str(e))
        elif browser == "safari":
            self.driverRaw = webdriver.Safari()
        else:
            self.driverRaw = self._initialize_chrome_driver(options=options)

        # Setting Driver Implicit Time out for An Element
        self.driver = EventFiringWebDriver(self.driverRaw, CustomBrowserListener())
        self.driver.implicitly_wait(3)
        # Maximize the window
        self.driver.maximize_window()
        # Loading browser with App URL
        self.driver.get(url)
        global_variables.driver = self.driver

    def close_browser(self):
        """
        Method to close Browser
        :param none
        :return none
        """
        global_variables.driver.quit()

    def get_url(self):
        """
        Method to get the current URL from Browser
        :param none
        :return url
        """
        return self.driverRaw.current_url

    def refresh(self):
        """
        Method to refresh browser page
        :param none
        :return none
        """
        global_variables.driver.refresh()

    def prepare_opened_browser(self, guest_mode: bool = False):
        """
        Method to close all chrome browsers and open instance on port 9229
        :param none
        :return none
        """
        self.close_all_browsers()
        if get_custom_platform() == "windows":
            if guest_mode:
                os.system("start chrome --remote-debugging-port=9229 --guest --lang='en' --disable-search-engine-choice-screen")
            else:
                os.system("start chrome --remote-debugging-port=9229")
        else:
            if guest_mode:
                path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                subprocess.Popen([path, '--args', '--remote-debugging-port=9229', '--guest', "--lang='en'", '--disable-search-engine-choice-screen'])
            else:
                os.system("open /Applications/Google\ Chrome.app --args --remote-debugging-port=9229")
        time.sleep(2)

    def close_all_browsers(self):
        """
        Method to close all chrome browsers
        :param none
        :return none
        """
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if 'chrome.exe' in proc.name():
                    os.system("Taskkill /f /IM chrome.exe")
                if 'firefox.exe' in proc.name():
                    os.system("Taskkill /f /IM firefox.exe")
        else:
            os.system('pkill Chrome')
            os.system('pkill firefox')
        time.sleep(5)

    def connect_to_google_accounts_browser_page(self):
        """
        Method to connect to browser instance opened on port 9229 and switch to Google Accounts sign in page
        :param none
        :return driver
        """
        time.sleep(2)

        driver = self._initialize_chrome_driver()

        handles = driver.window_handles
        handle_flag = False

        for handle in handles:
            driver.switch_to.window(handle)
            if 'accounts.google.com' in str(driver.current_url).lower():
                handle_flag = True
                break
        if handle_flag == False:
            driver.switch_to.window(handles[-1])
        driver.implicitly_wait(3)
        global_variables.driver = EventFiringWebDriver(driver, CustomBrowserListener())
        return global_variables.driver

    def connect_to_outlook_accounts_browser_page(self) -> EventFiringWebDriver:
        """
        Method to connect to browser instance opened on port 9229 and switch to Outlook Accounts sign in page
        :param none
        :return driver
        """
        time.sleep(2)
        driver = self._initialize_chrome_driver()
        handles = driver.window_handles
        handle_flag = False
        for handle in handles:
            driver.switch_to.window(handle)
            if 'login.microsoftonline.com' in str(driver.current_url).lower():
                handle_flag = True
                break
        if handle_flag == False:
            driver.switch_to.window(handles[-1])
        driver.implicitly_wait(3)
        global_variables.driver = EventFiringWebDriver(driver, CustomBrowserListener())
        return global_variables.driver

    def connect_to_outlook_calendar_browser_page(self) -> EventFiringWebDriver:
        """
        Method to connect to browser instance opened on port 9229 and switch to Outlook Accounts sign in page
        :param none
        :return driver
        """
        time.sleep(2)
        driver = self._initialize_chrome_driver()
        driver.get("https://outlook.live.com/calendar/0/view/month")
        handles = driver.window_handles
        handle_flag = False
        for handle in handles:
            driver.switch_to.window(handle)
            if 'outlook.live.com/calendar' in str(driver.current_url).lower():
                handle_flag = True
                break
        if handle_flag == False:
            driver.switch_to.window(handles[-1])
        driver.implicitly_wait(3)
        global_variables.driver = EventFiringWebDriver(driver, CustomBrowserListener())
        return global_variables.driver

    def connect_to_support_browser_page(self) -> EventFiringWebDriver:
        """
        Method to connect to browser instance opened on port 9229 and switch to Support page
        :param none
        :return driver
        """
        time.sleep(2)
        driver = self._initialize_chrome_driver()
        driver.maximize_window()
        handles = driver.window_handles
        handle_flag = False
        for handle in handles:
            driver.switch_to.window(handle)
            if 'prosupport.logi.com' in str(driver.current_url).lower():
                handle_flag = True
                break
        if handle_flag == False:
            driver.switch_to.window(handles[-1])
        driver.implicitly_wait(3)
        global_variables.driver = EventFiringWebDriver(driver, CustomBrowserListener())
        return global_variables.driver
    
    def connect_to_share_feedback_browser_page(self) -> EventFiringWebDriver:
        """
        Method to connect to browser instance opened on port 9229 and switch to Share feedback page
        :param none
        :return driver
        """
        time.sleep(2)
        driver = self._initialize_chrome_driver()
        driver.maximize_window()
        handles = driver.window_handles
        handle_flag = False
        for handle in handles:
            driver.switch_to.window(handle)
            if 'feedback.userreport.com' in str(driver.current_url).lower():
                handle_flag = True
                break
        if handle_flag == False:
            driver.switch_to.window(handles[-1])
        driver.implicitly_wait(3)
        global_variables.driver = EventFiringWebDriver(driver, CustomBrowserListener())
        return global_variables.driver

    def connect_to_current_browser_page(self):
        """
        Method to connect to browser instance opened on port 9229 and switch to last opened tab
        :param none
        :return driver
        """
        time.sleep(2)
        driver = self._initialize_chrome_driver()
        handles = driver.window_handles
        driver.switch_to.window(handles[0])
        driver.implicitly_wait(3)
        return driver

