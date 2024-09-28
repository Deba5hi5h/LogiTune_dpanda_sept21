from apps.tune_mobile.config import tune_mobile_config
from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from base.base_ui import UIBase
from locators.tune_mobile.tune_mobile_device_name_locators import TuneMobileDeviceNameLocators


class TuneMobileDeviceName(TuneMobile):

    def click_close(self) -> TuneMobileHome:
        """
        Method to click close button

        :param :
        :return TuneMobileHome:
        """
        UIBase.elementName = "Close"

        self.find_element(TuneMobileDeviceNameLocators.CLOSE).click()
        return TuneMobileHome()

    def click_update(self) -> TuneMobileHome:
        """
        Method to click Update button

        :param :
        :return TuneMobileHome:
        """
        UIBase.elementName = "Update"
        self.find_element(TuneMobileDeviceNameLocators.UPDATE).click()
        return TuneMobileHome()

    def click_surprise_me(self):
        """
        Method to click Update button

        :param :
        :return TuneMobileDeviceName:
        """
        UIBase.elementName = "Surprise Me"
        self.find_element(TuneMobileDeviceNameLocators.DEVICE_NAME_TEXTFIELD).clear()
        self.find_element(TuneMobileDeviceNameLocators.SURPRISE_ME).click()
        return self

    def type_device_name(self, device_name: str):
        """
        Method to type text in device name text field

        :param device_name:
        :return TuneMobileDeviceName:
        """
        UIBase.elementName = "Device Name"
        element = self.find_element(TuneMobileDeviceNameLocators.DEVICE_NAME_TEXTFIELD)
        element.clear()
        element.send_keys(device_name)
        return self

    def get_device_name_value(self) -> str:
        """
        Method to get Device Name value

        :param :
        :return str:
        """
        value = 'value' if self.is_ios_device() else 'text'
        return self.find_element(TuneMobileDeviceNameLocators.DEVICE_NAME_TEXTFIELD).get_attribute(value)

    def verify_surprise_me_displayed(self) -> bool:
        """
        Method to verify Surprise Me link displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDeviceNameLocators.SURPRISE_ME, timeout=2)

    def verify_close_button_displayed(self) -> bool:
        """
        Method to verify Close button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDeviceNameLocators.CLOSE, timeout=2)

    def verify_update_button_displayed(self) -> bool:
        """
        Method to verify Update button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDeviceNameLocators.UPDATE, timeout=2)

    def verify_device_name_textfield_displayed(self) -> bool:
        """
        Method to verify Device Name Text Field displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDeviceNameLocators.DEVICE_NAME_TEXTFIELD, timeout=2)
