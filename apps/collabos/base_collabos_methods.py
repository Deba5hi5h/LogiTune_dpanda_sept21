from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from apps.collabos import collabos_config
from base import global_variables
from extentreport.report import Report


class CollabOsBaseMethods:

    @staticmethod
    def find_element_collabos(element, param=None, timeout=collabos_config.implicit_wait, visibility=True, skip_exception=False) -> WebElement:
        try:
            """
            Method to find element

            :param element:
            :return:
            """
            if param is not None:
                temp = list(element)
                temp[1] = temp[1].replace('XXX', param)
                element = tuple(temp)
            if visibility:
                WebDriverWait(global_variables.collabos_driver, timeout) \
                    .until(expected_conditions.visibility_of_element_located(element))
            else:
                WebDriverWait(global_variables.collabos_driver, timeout) \
                    .until(expected_conditions.presence_of_element_located(element))
            found_element = global_variables.collabos_driver.find_element(by=element[0], value=element[1])
            return found_element

        except Exception as e:
            if not skip_exception:
                Report.logException(f"Unable to find element- {element}", is_collabos=True)
                raise e
            else:
                return None

    @staticmethod
    def find_element_collabos_text_to_be_present(element, message, param=None, timeout=collabos_config.implicit_wait):
        try:
            """
            Method to find element

            :param element:
            :return:
            """
            if param is not None:
                temp = list(element)
                temp[1] = temp[1].replace('XXX', param)
                element = tuple(temp)
            WebDriverWait(global_variables.collabos_driver, timeout) \
                .until(expected_conditions.text_to_be_present_in_element(element, message))

            found_element = global_variables.collabos_driver.find_element(by=element[0], value=element[1])
            return found_element

        except Exception as e:
            Report.logException(f"Unable to find element- {element}", is_collabos=True)
            raise e

    @staticmethod
    def find_elements_collabos(element, param=None, timeout=collabos_config.implicit_wait, visibility=True):
        try:
            """
            Method to find element

            :param element:
            :return:
            """
            global_variables.collabos_driver.implicitly_wait(timeout)
            if param is not None:
                temp = list(element)
                temp[1] = temp[1].replace('XXX', param)
                element = tuple(temp)
            found_elements = global_variables.collabos_driver.find_elements(by=element[0], value=element[1])
            return found_elements

        except Exception as e:
            Report.logException(f"Unable to find element- {element}", is_collabos=True)
            raise e
        finally:
            global_variables.collabos_driver.implicitly_wait(collabos_config.implicit_wait)

    @staticmethod
    def verify_element_present_currently_collabos(element):
        try:
            global_variables.collabos_driver.find_element(*element)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def verify_element_collabos(element, param=None, timeout=collabos_config.implicit_wait, visibility=True):
        """
        Method to verify if an element exists
        :param element: timeunit in seconds
        :return: true/false
        """
        try:
            global_variables.collabos_driver.implicitly_wait(timeout)
            if param is not None:
                temp = list(element)
                temp[1] = temp[1].replace('XXX', param)
                element = tuple(temp)
            if visibility:
                WebDriverWait(global_variables.collabos_driver, timeout) \
                    .until(expected_conditions.visibility_of_element_located(element))
            else:
                WebDriverWait(global_variables.collabos_driver, timeout) \
                    .until(expected_conditions.presence_of_element_located(element))
            found_element = global_variables.collabos_driver.find_element(by=element[0], value=element[1])
            global_variables.collabos_driver.implicitly_wait(collabos_config.implicit_wait)
            return True
        except Exception as e:
            Report.logInfo(f"Unable to find element- {element}", is_collabos=True)
            global_variables.collabos_driver.implicitly_wait(collabos_config.implicit_wait)
            return False

    @staticmethod
    def scroll_to_element_by_resource_id(element):
        from appium.webdriver.common.appiumby import AppiumBy
        global_variables.collabos_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                      f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().resourceId("{element[1]}").instance(0));')
