import time

from apps.sync import sync_config
from apps.sync.sync_app import SyncApp
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_app.sync_app_device_locators import SyncAppDeviceLocators


class SyncDevice(SyncApp):

    def click_info(self):
        """
        Method to click on info icon in Sync App

        :param :
        :return SyncDevice:
        """
        UIBase.elementName = "Info"
        self.look_element(SyncAppDeviceLocators.INFO).click()
        return SyncDevice()

    def click_kebab(self):
        """
        Method to click on kebab icon in Sync App

        :param :
        :return SyncDevice:
        """
        UIBase.elementName = "Kebab"
        self.look_nth_element(SyncAppDeviceLocators.KEBAB, 1).click()
        time.sleep(1)
        return SyncDevice()

    def click_forget_device(self):
        """
        Method to click on Forget Device Kebab option

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.FORGET_DEVICE).click()
        return SyncDevice()

    def click_lets_fix_it(self):
        """
        Method to click on Let's Fix it

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.LETS_FIX_IT).click()
        return SyncDevice()

    def click_forget(self):
        """
        Method to click on Forget

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.FORGET).click()
        return SyncDevice()

    def click_forget_now(self):
        """
        Method to click on Forget Now button

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.FORGET_NOW).click()
        return SyncDevice()

    def click_update(self):
        """
        Method to click on Update button

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.UPDATE).click()
        return SyncDevice()

    def click_update_now(self):
        """
        Method to click on Update button

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.UPDATE_NOW).click()
        return SyncDevice()

    def click_check_for_device_update(self):
        """
        Method to click on Check for Device Update Kebab option

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.CHECK_FOR_DEVICE_UPDATE).click()
        return SyncDevice()

    def click_quick_start_guide(self):
        """
        Method to click on Quick Start Guide Kebab option

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.QUICK_START_GUIDE).click()
        return SyncDevice()

    def click_setup_video(self):
        """
        Method to click on Setup Video Kebab option

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.SETUP_VIDEO).click()
        return SyncDevice()

    def click_product_support(self):
        """
        Method to click on Product Support Kebab option

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.PRODUCT_SUPPORT).click()
        return SyncDevice()

    def click_order_spare_parts(self):
        """
        Method to click on Order Spare Parts Kebab option

        :param :
        :return SyncDevice:
        """
        self.look_element(SyncAppDeviceLocators.ORDER_SPARE_PARTS).click()
        return SyncDevice()

    def verify_check_for_device_update(self) -> bool:
        """
        Method to verify Check for Device Update option displayed in Kebab options

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.CHECK_FOR_DEVICE_UPDATE, timeunit=3)

    def verify_forget_device(self) -> bool:
        """
        Method to verify Forget Device displayed in Kebab options

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.FORGET_DEVICE)

    def verify_quick_start_guide(self) -> bool:
        """
        Method to verify Quick Start Guide displayed in Kebab options

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.QUICK_START_GUIDE, timeunit=3)

    def verify_setup_video(self) -> bool:
        """
        Method to verify Setup Video displayed in Kebab options

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.SETUP_VIDEO, timeunit=3)

    def verify_product_support(self) -> bool:
        """
        Method to verify Product Support displayed in Kebab options

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.PRODUCT_SUPPORT, timeunit=3)

    def verify_order_spare_parts(self) -> bool:
        """
        Method to verify Order Spare Parts displayed in Kebab options

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.ORDER_SPARE_PARTS, timeunit=3)

    def verify_device_connect_message(self, device_name: str) -> bool:
        """
        Method to verify device connected message displayed

        :param device_name:
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.DEVICE_CONNECT_MESSAGE, timeunit=60, param=device_name)

    def verify_device_disconnect_message(self, device_name: str) -> bool:
        """
        Method to verify device disconnected message displayed

        :param device_name:
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.DEVICE_DISCONNECT_MESSAGE, timeunit=50, param=device_name)

    def verify_device_error_message(self, device_name: str, timeout: int = 60) -> bool:
        """
        Method to verify problem with device error message displayed

        :param device_name:
        :param timeout:
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.DEVICE_ERROR_MESSAGE, timeunit=timeout, param=device_name)

    def verify_firmware_update_available(self) -> bool:
        """
        Method to verify firmware update available for device

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.UPDATE_AVAILABLE)

    def verify_firmware_update_failed(self) -> bool:
        """
        Method to verify firmware update failed for device

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.UPDATE_FAILED, timeunit=2)

    def verify_update_now_button(self) -> bool:
        """
        Method to verify Update Now button displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.UPDATE_NOW, timeunit=5)

    def verify_schedule_update_button(self) -> bool:
        """
        Method to verify Schedule Update button displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.SCHEDULE_UPDATE, timeunit=5)

    def verify_back_button(self) -> bool:
        """
        Method to verify Back button displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.BACK, timeunit=1)

    def verify_device_up_to_date(self, device_name: str) -> bool:
        """
        Method to verify Device Up to Date message displayed

        :param device_name:
        :return bool:
        """
        return self.verify_element(SyncAppDeviceLocators.DEVICE_UPDATE_MESSAGE, param=device_name)

    def verify_swycth_connected_to_external_pc_message_displayed(self, displayed: bool = True) -> bool:
        """
        Method to verify Swytch is connected to an external computer message displayed

        :param displayed:
        :return bool:
        """
        i = sync_config.SYNC_TIMEOUT
        while i > 0:
            if displayed and self.verify_element(SyncAppDeviceLocators.SWYTCH_CONNECTED_TO_EXTERNAL_PC, timeunit=1):
                return True
            elif not displayed and not self.verify_element(SyncAppDeviceLocators.SWYTCH_CONNECTED_TO_EXTERNAL_PC,
                                                           timeunit=1):
                return True
            i = i - 1
            time.sleep(1)
        return False

    def verify_swytch_byod_device_status_message_displayed(self, displayed: bool = True) -> bool:
        """
        Method to verify Status unknown since the device has been connected to an external computer  message displayed

        :param displayed:
        :return bool:
        """
        i = sync_config.SYNC_TIMEOUT
        while i > 0:
            if displayed and self.verify_element(SyncAppDeviceLocators.SWYTCH_BYOD_DEVICE_STATUS, timeunit=1):
                return True
            elif not displayed and not self.verify_element(SyncAppDeviceLocators.SWYTCH_BYOD_DEVICE_STATUS,
                                                           timeunit=1):
                return True
            i = i - 1
            time.sleep(1)
        return False

    def verify_swytch_byod_device_settings_message_displayed(self, displayed: bool = True) -> bool:
        """
        Method to verify Settings can not be modified now since the device has been connected to an
        external computer message displayed

        :param displayed:
        :return bool:
        """
        i = sync_config.SYNC_TIMEOUT
        while i > 0:
            if displayed and self.verify_element(SyncAppDeviceLocators.SWYTCH_BYOD_DEVICE_SETTINGS, timeunit=1):
                return True
            elif not displayed and not self.verify_element(SyncAppDeviceLocators.SWYTCH_BYOD_DEVICE_SETTINGS,
                                                           timeunit=1):
                return True
            i = i - 1
            time.sleep(1)
        return False

    def get_device_information(self, device_name: str) -> dict:
        """
        Method to get Device information displayed from Sync App

        :param device_name:
        :return dict:
        """
        self.click_info()
        device_info = {}
        try:
            Report.logPass(f"Capturing {device_name} Information from Sync App", True)
            if device_name.upper() in ("RALLY BAR", "RALLY BAR MINI"):
                device_info["serial_sumber"] = self.look_element(SyncAppDeviceLocators.SERIAL_NUMBER).text
                device_info["logi_collabos"] = self.look_element(SyncAppDeviceLocators.LOGI_COLLABOS).text
                device_info["firmware_version"] = self.look_element(SyncAppDeviceLocators.FIRMWARE_VERSION).text
                device_info["system_image"] = self.look_element(SyncAppDeviceLocators.SYSTEM_IMAGE).text
                device_info["audio"] = self.look_element(SyncAppDeviceLocators.AUDIO).text
                device_info["house_keeping"] = self.look_element(SyncAppDeviceLocators.HOUSEKEEPING).text
                device_info["pan_tilt"] = self.look_element(SyncAppDeviceLocators.PAN_TILT).text
                device_info["zoom_focus"] = self.look_element(SyncAppDeviceLocators.ZOOM_FOCUS).text
            elif device_name.upper() == "RALLY CAMERA":
                device_info["PID"] = self.look_element(SyncAppDeviceLocators.PID).text
                device_info["BLE_Firmware"] = self.look_element(SyncAppDeviceLocators.BLE_FIRMWARE_RALLY_CAM).text
                device_info["EEPROM_Firmware"] = self.look_element(SyncAppDeviceLocators.EEPROM_FIRMWARE_RALLY_CAM).text
                device_info["Video_Firmware"] = self.look_element(SyncAppDeviceLocators.VIDEO_FIRMWARE_RALLY_CAM).text
            else:
                device_info["PID"] = self.look_element(SyncAppDeviceLocators.PID).text
                device_info["BLE_Firmware"] = self.look_element(SyncAppDeviceLocators.BLE_FIRMWARE).text
                device_info["EEPROM_Firmware"] = self.look_element(SyncAppDeviceLocators.EEPROM_FIRMWARE).text
                device_info["Video_Firmware"] = self.look_element(SyncAppDeviceLocators.VIDEO_FIRMWARE).text
            if device_name.upper() == "MEETUP":
                device_info["Audio_Firmware"] = self.look_element(SyncAppDeviceLocators.AUDIO_FIRMWARE).text
                device_info["Codec_Firmware"] = self.look_element(SyncAppDeviceLocators.CODEC_FIRMWARE).text

        except Exception as e:
            Report.logException(f"Capturing {device_name} Information from Sync App failed: {e}")
        UIBase.report_flag = False
        self.press_esc_key()
        return device_info
