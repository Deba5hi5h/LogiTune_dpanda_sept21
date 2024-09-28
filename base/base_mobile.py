import os
import logging
from pathlib import Path

from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from apps.tune_mobile.config import tune_mobile_config
from base import global_variables
from base.base import Base
from common.aws_wrappers import SSMParameterStore
from config.aws_helper import AWSHelper
from extentreport.report import Report

log = logging.getLogger(__name__)


class MobileBase(Base):
    elementName = ""
    test_flag = True
    rootPath = Path(os.path.dirname(__file__)).parent
    driver = None
    device = tune_mobile_config.phone
    appium_service = AppiumService()

    @classmethod
    def setUpClass(cls) -> None:
        # Logging for Webdriver set to Error only
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
        # cls.appium_service.start()
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
        if global_variables.setupFlag:
            global_variables.PLATFORM_NAME = MobileBase.get_platform_name()
            global_variables.PLATFORM_VERSION = MobileBase.get_platform_version()
            super(MobileBase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super(MobileBase, cls).tearDownClass()
        # cls.appium_service.stop()

    def setUp(self) -> None:
        Base.setUp(self)
        testName = self.__getattribute__("_testMethodName")
        print("*" * 100)
        print("Executing Test: " + testName)

    def tearDown(self) -> None:
        Base.tearDown(self)
        if tune_mobile_config.phone == "OnePlus":
            try:
                global_variables.driver.quit()
            except:
                pass
            global_variables.driver = None
        if MobileBase.test_flag != True:
            assert False

    def find_element(self, element, param=None, timeout=tune_mobile_config.implicit_wait, visibility=True):
        try:
            """
            Method to find element

            :param element:
            :return:
            """
            if self.is_ios_device():
                locator = element[0]
            else:
                locator = element[1]
            if param is not None:
                temp = list(locator)
                temp[1] = temp[1].replace('XXX', param)
                locator = tuple(temp)
            if visibility:
                WebDriverWait(global_variables.driver, timeout) \
                    .until(expected_conditions.visibility_of_element_located(locator))
            else:
                WebDriverWait(global_variables.driver, timeout) \
                    .until(expected_conditions.presence_of_element_located(locator))
            found_element = global_variables.driver.find_element(*locator)
            return found_element

        except Exception as e:
            print("Unable to find element- {}".format(element))
            raise e

    def find_elements(self, element, param=None, timeout=tune_mobile_config.implicit_wait):
        try:
            """
            Method to find elements

            :param element:
            :return:
            """
            global_variables.driver.implicitly_wait(timeout)
            if self.is_ios_device():
                locator = element[0]
            else:
                locator = element[1]
            if param is not None:
                temp = list(locator)
                temp[1] = temp[1].replace('XXX', param)
                locator = tuple(temp)
            found_elements = global_variables.driver.find_elements(*locator)
            global_variables.driver.implicitly_wait(tune_mobile_config.implicit_wait)
            return found_elements
        except Exception as e:
            global_variables.driver.implicitly_wait(tune_mobile_config.implicit_wait)
            print("Unable to find element- {}".format(element))
            raise e

    def verify_element(self, element, param=None, timeout=tune_mobile_config.implicit_wait, visibility=True):
        """
        Method to verify if an element exists
        :param element: timeunit in seconds
        :return: true/false
        """
        try:
            global_variables.driver.implicitly_wait(timeout)
            if self.is_ios_device():
                locator = element[0]
            else:
                locator = element[1]
            if param is not None:
                temp = list(locator)
                temp[1] = temp[1].replace('XXX', param)
                locator = tuple(temp)
            if visibility:
                WebDriverWait(global_variables.driver, timeout) \
                    .until(expected_conditions.visibility_of_element_located(locator))
            else:
                WebDriverWait(global_variables.driver, timeout) \
                    .until(expected_conditions.presence_of_element_located(locator))
            found_element = global_variables.driver.find_element(*locator)
            global_variables.driver.implicitly_wait(tune_mobile_config.implicit_wait)
            return True
        except Exception as e:
            global_variables.driver.implicitly_wait(tune_mobile_config.implicit_wait)
            return False

    def swipe(self, direction: str, element=None):
        if element is not None:
            size = element.size
        else:
            size = global_variables.driver.get_window_size()
        startX = endX = startY = endY = 0
        if direction.lower() == "down":
            startX = endX = int(size["width"] / 2)
            startY = int(size["height"] * 0.6)
            endY = int(size["height"] * 0.9)
        elif direction.lower() == "up":
            startX = endX = int(size["width"] / 2)
            startY = int(size["height"] * 0.7)
            endY = int(size["height"] * 0.4)
        elif direction.lower() == "left":
            startY = endY = int(size["height"] / 2)
            startX = int(size["width"] * 0.05)
            endX = int(size["width"] * 0.9)
        elif direction.lower() == "right":
            startY = endY = int(size["height"] / 2)
            startX = int(size["width"] * 0.9)
            endX = int(size["width"] * 0.05)

        action = TouchAction(global_variables.driver)
        if element is not None:
            action.press(el=element, x=startX, y=startY).wait(2000).move_to(x=endX, y=endY).release().perform()
        else:
            action.press(x=startX, y=startY).wait(1000).move_to(x=endX, y=endY).perform()

    def drag(self, element, direction: str, end: float):
        size = element.size
        x = element.location['x']
        y = element.location['y']
        startX = endX = startY = endY = 0
        if direction.lower() == "vertical":
            startX = endX = int(size["width"] / 2)
            startY = int(size["height"] * 0.5)
            endY = y + end
        elif direction.lower() == "horizontal":
            startY = endY = int(size["height"] / 2)
            startX = int(size["width"] * 0.5)
            endX = x + end

        action = TouchAction(global_variables.driver)
        action.press(el=element, x=startX, y=startY).wait(2000).move_to(x=endX, y=endY).release().perform()

    def swipe_screen(self, direction: str, start: float, end: float):

        size = global_variables.driver.get_window_size()
        startX = endX = startY = endY = 0
        if direction.lower() == "vertical":
            startX = endX = int(size["width"] / 2)
            startY = int(size["height"] * start)
            endY = int(size["height"] * end)
        elif direction.lower() == "horizontal":
            startY = endY = int(size["height"] / 2)
            startX = int(size["width"] * start)
            endX = int(size["width"] * end)

        if self.is_android_device():
            global_variables.driver.swipe(startX, startY, endX, endY)
        else:
            action = TouchAction(global_variables.driver)
            action.press(x=startX, y=startY).wait(2000).move_to(x=endX, y=endY).perform()

    def adjust_slider(self, element, value: int):
        height = element.rect['height']
        width = element.rect['width']
        startX = endX = element.rect['x'] + (width / 2)
        startY = element.rect['y'] + (height / 2)

        endY = startY - value
        action = TouchAction(global_variables.driver)
        action.press(x=startX, y=startY).wait(500).move_to(x=endX, y=endY).release().perform()

    def adjust_slider_android(self, element, value: int):
        height = element.rect['height']
        width = element.rect['width']
        current_value = int(float(element.text))
        startX = endX = element.rect['x']
        startY = element.rect['y'] + 128 - current_value + height / 2
        if value < 0:
            endY = startY - value
        else:
            value *= 3.5
            endY = startY - value
        action = TouchAction(MobileBase.driver)
        action.press(x=startX, y=startY).wait(500).move_to(x=endX, y=endY).release().perform()

    def touch_element(self, element, param=None, visibility=False):
        """
        Method to tap on element
        :param element:
        :param param:
        :param visibility:
        :return:
        """
        try:
            el = self.find_element(element, param=param, visibility=visibility)
            actions = TouchAction(MobileBase.driver)
            actions.press(el, el.location['x'], el.location['y']).release().perform()
        except Exception as e:
            print(f"Unable to perform touch element- {e}")

    def tap_element(self, element, param=None, visibility=False):
        """
        Method to tap on element
        :param element:
        :param param:
        :param visibility:
        :return:
        """
        try:
            el = self.find_element(element, param=param, visibility=visibility)
            actions = TouchAction(global_variables.driver)
            actions.tap(element, el.location['x'], el.location['y'], 1)
        except Exception as e:
            print(f"Unable to perform tap on element- {element}")

    def tap_by_coordinates(self, x: int, y: int):
        """
        Method to tap on element by x and y coordinates
        :param x:
        :param y:
        :return:
        """
        try:
            actions = TouchAction(global_variables.driver)
            actions.tap(x=x, y=y).perform()
        except Exception as e:
            print(f"Unable to perform tap by coordinates {x} and {y}")

    def drag_down_by_coordinates(self, x: int, y: int):
        """
        Method to drag on element by x and y coordinates
        :param x:
        :param y:
        :return:
        """
        try:
            actions = TouchAction(global_variables.driver)
            actions.press(x=x, y=y).wait(500).move_to(x=x, y=y + 200).release().perform()
        except Exception as e:
            print(f"Unable to perform drag by coordinates {x} and {y}")

    def touch_screen(self):
        """
        Method to tap on middle of the screen
        :param element: timeunit in seconds
        :return:
        """
        try:
            size = global_variables.driver.get_window_size()
            x = int(size["width"] / 2)
            y = int(size["height"] / 2)
            self.tap_by_coordinates(x, y)
        except Exception as e:
            print("Unable to perform touch screen")

    def scroll_wheel(self, element, direction: str = "up"):
        """
        Method to tap on middle of the screen
        :param element: timeunit in seconds
        :return:
        """
        try:
            params = {}
            params['order'] = "next" if direction is "up" else "previous"
            params['offset'] = 0.15
            params['element'] = element
            global_variables.driver.execute_script("mobile: selectPickerWheelValue", params)
        except Exception as e:
            print("Unable to scroll wheel")

    @staticmethod
    def get_platform_name() -> str:
        """
        Method to get the platform name of the device in test
        :param :
        :return str:
        """
        return tune_mobile_config.device.get(MobileBase.device).get("platform_name")

    @staticmethod
    def get_platform_version() -> str:
        """
        Method to get the platform version of the device in test
        :param :
        :return str:
        """
        return tune_mobile_config.device.get(MobileBase.device).get("platform_version")

    @staticmethod
    def get_udid() -> str:
        """
        Method to get the udid of the device in test
        :param :
        :return str:
        """
        return tune_mobile_config.device.get(MobileBase.device).get("udid")

    @staticmethod
    def get_model() -> str:
        """
        Method to get the model of the device in test
        :param :
        :return str:
        """
        return tune_mobile_config.device.get(MobileBase.device).get("model")

    @staticmethod
    def get_passcode() -> str:
        """
        Method to get the passcode of the device in test
        :param :
        :return str:
        """
        return tune_mobile_config.device.get(MobileBase.device).get("passcode")

    @staticmethod
    def is_ios_device() -> bool:
        """
        Method to check if device under test is iOS
        :param :
        :return bool:
        """
        return True if MobileBase.get_platform_name().lower() == 'ios' else False

    @staticmethod
    def is_android_device() -> bool:
        """
        Method to check if device under test is iOS
        :param :
        :return bool:
        """
        return True if MobileBase.get_platform_name().lower() == 'android' else False
