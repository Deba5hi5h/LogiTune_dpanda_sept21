import logging
import psutil
import os
import time
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from apps.tune.helpers import get_python_version
from base import global_variables, base_settings
from pathlib import Path
from base.base import Base
from common.framework_params import PROJECT
from common.platform_helper import get_custom_platform
from common.proxy import Proxy
from config.aws_helper import AWSHelper
from extentreport.report import Report
from common.logs_storer import store_failed_testcase_logs_on_server

from common.aws_wrappers import SSMParameterStore


log = logging.getLogger(__name__)


class UIBase(Base):
    elementName = ""
    send_keys_value = ""
    rootPath = Path(os.path.dirname(__file__)).parent
    start_timer=None
    report_flag = True
    highlight_flag = True
    logi_tune_flag = False

    @classmethod
    def setUpClass(cls, start_winappdriver=True) -> None:
        #Logging for Webdriver set to Error only
        logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        logger.setLevel(logging.ERROR)
        logger = logging.getLogger('urllib3.connectionpool')
        logger.setLevel(logging.ERROR)
        logger = logging.getLogger('urllib3.util.retry')
        logger.setLevel(logging.ERROR)
        logger = logging.getLogger('PIL.PngImagePlugin')
        logger.setLevel(logging.ERROR)
        logger = logging.getLogger('paramiko.transport')
        logger.setLevel(logging.INFO)
        if global_variables.setupFlag:
            super(UIBase, cls).setUpClass()

            #UI Tests Specific
            if start_winappdriver:
                if get_custom_platform() == "windows":
                    os.system(str(UIBase.rootPath) + "\\WinApp\\winapp.bat")
                    if global_variables.ENABLE_PROXY:
                        Proxy.add_outbound_rule_for_hosts()

            cls.aws_config_file = None
            cls.role = global_variables.SYNC_ROLE
            cls.env = global_variables.SYNC_ENV
            global_variables.config = AWSHelper.get_config(global_variables.SYNC_ENV)
            if global_variables.config is None:
                try:
                    prefix = '/seam/raiden/' + cls.env + '/'
                    log.info(f'Prefix is {prefix}')
                    cls.ssm_ps_wrapper = SSMParameterStore(
                        prefix=prefix, aws_config_file=cls.aws_config_file)
                except Exception as e:
                    log.error(
                        'Unable to fetch SSM Credentials. Make sure AWS credentials are set properly')
                    raise e

                try:
                    global_variables.config = cls.ssm_ps_wrapper.get_parameter_value_as_struct('config')
                except Exception as e:
                    log.error('Exception while reading config: {}'.format(e))

    @classmethod
    def tearDownClass(cls) -> None:
        super(UIBase, cls).tearDownClass()
        # Close WinAppDriver on Windows
        if global_variables.teardownFlag == True and get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if 'WinAppDriver.exe' in proc.name():
                    print(f'Killing {proc.name()}')
                    proc.kill()

    def setUp(self) -> None:
        Base.setUp(self)
        testName = self.__getattribute__("_testMethodName")
        print("*" * 100)
        print("Executing Test: " + testName)

    def tearDown(self) -> None:
        if PROJECT == 'LogiTune':
            if global_variables.testStatus == 'Fail' and "update" not in self.id():
                self.tune_app.save_logitune_logs_in_testlogs(testlogs_path=self.logdirectory, test_name=self.id())
        print("Completed Test: " + self.id())
        Base.tearDown(self)

        try:
            if not UIBase.logi_tune_flag:
                global_variables.driver.quit()
        except:
            print("Application is already closed")

    def look_element(self, element, param=None, timeout=base_settings.IMPLICIT_WAIT, scroll_flag=True,
                     skip_exception=False, wait_for_visibility=False) -> WebElement:
        try:
            """
            Method to look for an element

            :param element:
            :return:
            """
            if param is not None:
                temp = list(element)
                temp[1] = temp[1].replace('XXX', param)
                element = tuple(temp)
            if wait_for_visibility:
                WebDriverWait(global_variables.driver, timeout).until(
                    expected_conditions.visibility_of_element_located(element))
            else:
                WebDriverWait(global_variables.driver, timeout).until(
                    expected_conditions.presence_of_element_located(element))
            found_element = global_variables.driver.find_element(*element)
            if get_python_version() >= 312:
                from apps.win_app_driver_reworked import element_json_to_web_element
                found_element = element_json_to_web_element(global_variables.driver, found_element)
            try:
                if scroll_flag:
                    global_variables.driver.execute_script("arguments[0].scrollIntoView(false); ", found_element)
            except:
                print("Cannot scroll into view")
            return found_element

        except Exception as e:
            if not skip_exception:
                Report.logException("Unable to find element- {}".format(element))
                raise e
            else:
                pass

    def look_clickable_element(self, element, param=None, timeout=base_settings.IMPLICIT_WAIT, scroll_flag=True,
                     skip_exception=True) -> WebElement:
        try:
            """
            Method to look for an element

            :param element:
            :return:
            """
            if param is not None:
                temp = list(element)
                temp[1] = temp[1].replace('XXX', param)
                element = tuple(temp)
            WebDriverWait(global_variables.driver, timeout).until(
                expected_conditions.element_to_be_clickable(element))
            found_element = global_variables.driver.find_element(*element)
            if get_python_version() >= 312:
                from apps.win_app_driver_reworked import element_json_to_web_element
                found_element = element_json_to_web_element(global_variables.driver, found_element)
            try:
                if scroll_flag:
                    global_variables.driver.execute_script("arguments[0].scrollIntoView(false); ", found_element)
            except:
                print("Cannot scroll into view")
            return found_element

        except Exception as e:
            if not skip_exception:
                Report.logException("Unable to find element- {}".format(element))
                raise e
            else:
                pass

    def look_elements(self, element_first, element_second, timeout=base_settings.IMPLICIT_WAIT,
                      second_element_exception=True, scroll_flag=True):
        found_element = None

        def element_find(driver):
            nonlocal found_element
            first = expected_conditions.presence_of_element_located(element_first)
            second = expected_conditions.presence_of_element_located(element_second)
            if first or second:
                for item in (element_first, element_second):
                    try:
                        found_element = global_variables.driver.find_element(*item)
                        if item == element_second and second_element_exception:
                            Report.logException(f"Wrong prompt occurred - {item}")
                            raise ValueError
                        return True
                    except NoSuchElementException:
                        pass
                    except ValueError as e:
                        raise e
                    except Exception as e:
                        Report.logException(f"Exception while handling element - {item}")
                        raise e
                return False
            else:
                return False

        try:
            WebDriverWait(global_variables.driver, timeout) \
                .until(element_find)
            try:
                if scroll_flag:
                    global_variables.driver.execute_script("arguments[0].scrollIntoView(false); ",
                                                           found_element)
            except Exception as e:
                print(f"Cannot scroll into view - {e}")
            return found_element
        except ValueError as e:
            Report.logException("Try Again prompt occurred.")
            raise e
        except TimeoutException as e:
            Report.logException(f"Unable to find elements - {element_first, element_second}. "
                                f"Timeout occurred after {timeout}s.")
            raise e
        except Exception as e:
            Report.logException(f"Unable to find elements - {element_first, element_second}")
            raise e

    def look_element_name(self, name):
        try:
            """
            Method to look for an element

            :param element:
            :return:
            """
            found_element = global_variables.driver.find_element(By.NAME, name)
            if get_python_version() >= 312:
                from apps.win_app_driver_reworked import element_json_to_web_element
                found_element = element_json_to_web_element(global_variables.driver, found_element)
            return found_element

        except Exception as e:
            Report.logException("Unable to find element by Name- {}".format(name))
            raise e

    def verify_element(self, element, timeunit=base_settings.IMPLICIT_WAIT, param=None, wait_for_visibility=False):
        """
        Method to verify if an element exists
        :param element: timeunit in seconds
        :return: true/false
        """
        try:
            if param is not None:
                temp = list(element)
                temp[1] = temp[1].replace('XXX', param)
                element = tuple(temp)

            global_variables.driver.implicitly_wait(timeunit)
            if wait_for_visibility:
                WebDriverWait(global_variables.driver, timeunit).until(
                    expected_conditions.visibility_of_element_located(element))
            found_element = global_variables.driver.find_element(*element)
            if get_python_version() >= 312:
                from apps.win_app_driver_reworked import element_json_to_web_element
                found_element = element_json_to_web_element(global_variables.driver, found_element)
            global_variables.driver.implicitly_wait(base_settings.IMPLICIT_WAIT)
            try:
                self.highLightElement(found_element)
                # global_variables.driver.execute_script("arguments[0].scrollIntoView(false); ", found_element)
            except:
                print("Cannot highlight/scroll into element")
            return True

        except Exception as e:
            global_variables.driver.implicitly_wait(base_settings.IMPLICIT_WAIT)
            return False

    @staticmethod
    def verify_element_not_visible(element, timeunit=base_settings.IMPLICIT_WAIT, param=None):
        """
        Method to verify if an element exists
        :param element: timeunit in seconds
        :return: true/false
        """
        try:
            if param is not None:
                temp = list(element)
                temp[1] = temp[1].replace('XXX', param)
                element = tuple(temp)

            global_variables.driver.implicitly_wait(timeunit)
            WebDriverWait(global_variables.driver, timeunit).until_not(
                    expected_conditions.visibility_of_element_located(element))
            global_variables.driver.implicitly_wait(base_settings.IMPLICIT_WAIT)
            return True

        except Exception as e:
            global_variables.driver.implicitly_wait(base_settings.IMPLICIT_WAIT)
            return False

    def verify_element_by_text(self, element, expected_text, timeout=10):
        """
        Method to verify if an element exists with text
        :param element: timeunit in seconds
        :return: true/false
        """
        def visibility_elements_check(_drv):
            elements = _drv.find_elements(*element)
            for el in elements:
                if el.text == expected_text:
                    return el
            return False
        try:
            found_element = WebDriverWait(global_variables.driver, timeout
                                          ).until(visibility_elements_check)
            if get_python_version() >= 312:
                from apps.win_app_driver_reworked import element_json_to_web_element
                found_element = element_json_to_web_element(global_variables.driver, found_element)
            try:
                self.highLightElement(found_element)
            except:
                print("Cannot highlight/scroll into element")
            return found_element

        except Exception as e:
            return False

    def verify_element_withwait(self, element, timeunit=base_settings.IMPLICIT_WAIT, param=None):
        """
        Method to verify if an element exists
        :param element: timeunit in seconds
        :return: true/false
        """
        if param is not None:
            temp = list(element)
            temp[1] = temp[1].replace('XXX', param)
            element = tuple(temp)

        while timeunit > 0:
            try:
                found_element = global_variables.driver.find_element(*element)
                if get_python_version() >= 312:
                    from apps.win_app_driver_reworked import element_json_to_web_element
                    found_element = element_json_to_web_element(global_variables.driver, found_element)
                try:
                    self.highLightElement(found_element)
                except:
                    print("Cannot highlight element")
                return True
            except:
                --timeunit
        return False

    def verify_element_name(self, name, timeunit=base_settings.IMPLICIT_WAIT):
        """
        Method to verify if an element exists by name

        :param element: timeunit in seconds
        :return: true/false
        """
        try:
            global_variables.driver.implicitly_wait(timeunit)
            global_variables.driver.find_element(By.NAME, name)
            global_variables.driver.implicitly_wait(base_settings.IMPLICIT_WAIT)
            return True

        except Exception as e:
            global_variables.driver.implicitly_wait(base_settings.IMPLICIT_WAIT)
            return False

    def look_nth_element(self, element, position):
        """
        Method to look for an element from n identical elements

        :param element:
        :return:
        """
        try:
            # Let there are n identical elements in DOM.
            # look_nth_element method finds the element at the given nth position
            WebDriverWait(global_variables.driver, base_settings.IMPLICIT_WAIT) \
                .until(expected_conditions.presence_of_element_located(element))
            found_element = global_variables.driver.find_elements(*element)
            if get_python_version() >= 312:
                from apps.win_app_driver_reworked import element_json_to_web_element
                found_element = element_json_to_web_element(global_variables.driver, found_element)
            return found_element[position]

        except Exception as e:
            Report.logException("Unable to find element {}".format(element))
            raise e

    def look_all_elements(self, element):
        """
        Method to look for all elements

        :param element:
        :return:
        """
        try:
            found_elements = global_variables.driver.find_elements(*element)
            if get_python_version() >= 312:
                from apps.win_app_driver_reworked import element_json_to_web_element
                found_elements = element_json_to_web_element(global_variables.driver, found_elements)
            return found_elements

        except Exception as e:
            Report.logException("Unable to find element {}".format(element))
            raise e

    def look_element_by_text(self, element, text):
        """
        Method to look for an element from n identical elements

        :param element:
        :return:
        """
        try:
            # Let there are n identical elements in DOM.
            # look_nth_element method finds the element at the given nth position
            WebDriverWait(global_variables.driver, base_settings.IMPLICIT_WAIT) \
                .until(expected_conditions.presence_of_element_located(element))
            found_element = global_variables.driver.find_elements(*element)
            if get_python_version() >= 312:
                from apps.win_app_driver_reworked import element_json_to_web_element
                found_element = element_json_to_web_element(global_variables.driver, found_element)
            for e in found_element:
                if str(e.text).upper() == str(text).upper():
                    return e
            return None

        except Exception as e:
            Report.logException("Unable to find element {}".format(element))
            raise e

    def wait_and_check_the_presence_of_element(self, element):
        """
        Method to wait and check the presence of element.
        Can be used to look for elements like Notifications which disappear quickly.
        :param element:
        :return:
        """
        try:
            log.info('Wait and check that the presence of element is located')
            WebDriverWait(global_variables.driver, base_settings.IMPLICIT_WAIT) \
                .until(expected_conditions.presence_of_element_located(element))

        except TimeoutException as e:
            Report.logException("Unable to look for the presence of element- {}".format(element))
            raise e

    def click_center(self, element, param=None):
        """
        Method to click center of an element.
        :param element:
        :param dynamic value
        :return:
        """
        e = self.look_element(element, param=param)
        size = e.size
        actions = ActionChains(global_variables.driver)
        actions.move_to_element_with_offset(e, size['width']/2, size['height']/2).click().perform()

    def scroll_down(self, element_locator, number_of_times=1):
        """
        Method to scroll page
        :param element_locator for clicking element before scroll
        :return:
        """
        try:
            global_variables.driver.find_element(*element_locator).click()
            i = 0
            while i < number_of_times:
                webdriver.ActionChains(global_variables.driver).send_keys(Keys.PAGE_DOWN).perform()
                i = i + 1
        except:
            print("Ignoring error in scrolling")


    def click_by_script(self, found_element):
        if UIBase.elementName != "":
            Report.logInfo("Clicking on element " + UIBase.elementName)
            UIBase.elementName = ""
        else:
            Report.logInfo("Clicking on element "+found_element.text)
        global_variables.driver.execute_script("arguments[0].click();", found_element)

    def start_performance_test(self):
        self.start_timer = time.time()
        self.previous_timer = self.start_timer

    def get_performance_time(self):
        elapsed_time = time.time() - self.previous_timer
        Report.logInfo("Time taken: "+time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        self.previous_timer = time.time()

    def end_performance_test(self, itemString):
        elapsed_time = time.time() - self.start_timer
        Report.logInfo("Total Time taken for "+itemString+" is " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

        return elapsed_time

    def highLightElement(self, element):
        if UIBase.highlight_flag == False:
            UIBase.highlight_flag = True
            return
        driver = element._parent
        if str(global_variables.driver.wrapped_driver).__contains__("appium"):
            return True
        def apply_style(s):
            current_style = element.get_attribute("style")
            driver.execute_script(f"arguments[0].setAttribute('style', `{current_style}; ${{arguments[1]}}`)",
                                  element, s)
        try:
            apply_style("border: {0}px solid {1};".format(5, "red"))
        except:
            print("Cannot highlight element: "+element)

    @staticmethod
    def press_esc_key():
        """
        Method to close the opened Kebab Menu

        :param none
        :return none
        """
        webdriver.ActionChains(global_variables.driver).send_keys(Keys.ESCAPE).perform()

    @staticmethod
    def press_enter_key():
        """
        Method to close the opened Kebab Menu
        :param none
        :return none
        """
        webdriver.ActionChains(global_variables.driver).send_keys(Keys.ENTER).perform()
