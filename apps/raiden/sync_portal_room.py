from time import time, sleep
from typing import Optional, Any

from selenium.webdriver.common.by import By

from apps.tune.logi_sync_personal_collab.utils import DEVICE_ONLINE_STATUS, DEVICE_OFFLINE_STATUS
from base import global_variables
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_portal.sync_portal_room_locators import SyncPortalRoomLocators


class SyncPortalRoom(UIBase):
    """
    Sync Portal Room Page test methods
    """

    def select_device(self, device_name: str):
        """
        Method to click on device from left panel in room

        :param device_name:str:
        :return:
        """
        self.look_element(SyncPortalRoomLocators.DEVICE_NAME, param=device_name).click()
        sleep(2)
        return self

    def select_device_audio(self, device_name: str):
        """
        Method to click on audio under device from left panel in room

        :param device_name:str:
        :return:
        """
        self.look_element(SyncPortalRoomLocators.DEVICE_AUDIO, param=device_name).click()
        sleep(2)
        return self

    def select_device_camera(self, device_name: str):
        """
        Method to click on Video under device from left panel in room

        :param device_name:str:
        :return:
        """
        self.look_element(SyncPortalRoomLocators.DEVICE_CAMERA, param=device_name).click()
        sleep(2)
        return self

    def select_device_connectivity(self, device_name: str):
        """
        Method to click on Connectivity under device from left panel in room

        :param device_name:str:
        :return:
        """
        self.look_element(SyncPortalRoomLocators.DEVICE_CONNECTIVITY, param=device_name).click()
        sleep(2)
        return self

    def select_computer(self):
        """
        Method to click on Computer from left panel in room

        :param :
        :return :
        """
        self.look_element(SyncPortalRoomLocators.COMPUTER).click()
        sleep(2)
        return self

    def select_room_checkbox(self, room_name: str):
        """
        Method to select Room checkbox in Inventory page

        :param : room_name: str
        :return :
        """
        self.look_element(SyncPortalRoomLocators.ROOM_CHECKBOX, param=room_name).click()
        return self

    def click_delete_button(self):
        """
        Method to click on Delete button

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.DELETE_BUTTON).click()
        return self

    def click_confirm_delete_yes_button(self):
        """
        Method to click on Yes button

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.CONFIRM_DELETE_YES).click()
        return self

    def click_anti_flicker_ntsc(self) -> None:
        """
        Method to set Anti flicker setting to NTSC

        :param none
        :return none
        """
        UIBase.elementName = "NTSC 60 Hz"
        e = self.look_element(SyncPortalRoomLocators.NTSC_60HZ)
        self.click_by_script(e)
        self.verify_anti_flicker_ntsc_selected(timeout=5)
        sleep(1)

    def click_anti_flicker_pal(self) -> None:
        """
        Method to set Anti flicker setting to PAL

        :param :
        :return :
        """
        UIBase.elementName = "PAL 50 Hz"
        e = self.look_element(SyncPortalRoomLocators.PAL_50HZ)
        self.click_by_script(e)
        self.verify_anti_flicker_pal_selected(timeout=5)
        sleep(1)

    def click_lets_fix_it(self):
        """
        Method to click on Let's Fix it

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.LETS_FIX_IT).click()
        sleep(1)
        return self

    def click_forget(self):
        """
        Method to click on Forget

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.FORGET).click()
        sleep(2)
        return self

    def click_forget_now(self):
        """
        Method to click on Forget Now

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.FORGET_NOW).click()
        return self

    def click_room_menu(self):
        """
        Method to click on Room Menu icon

        :param :
        :return : SyncPortalRoom
        """
        sleep(2)
        self.look_nth_element(SyncPortalRoomLocators.MENU_ICON, 2).click()
        return self

    def click_provision(self):
        """
        Method to click on Provision Tab

        :param :
        :return : SyncPortalRoom
        """
        sleep(2)
        self.look_element(SyncPortalRoomLocators.PROVISION_TAB, wait_for_visibility=True).click()
        return self

    def click_room_info(self):
        """
        Method to click on Room Info icon

        :param :
        :return : SyncPortalRoom
        """
        sleep(2)
        self.look_nth_element(SyncPortalRoomLocators.INFO_ICON, 0).click()
        return self

    def click_room_menu_provision_code(self):
        """
        Method to click on Provision Code under Room Menu

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.MENU_PROVISION_CODE).click()
        return self

    def click_page(self):
        """
        Method to click on Provision Code under Room Menu

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.ROOT).click()

    def type_in_confirm_delete_textbox(self, text: str):
        """
        Method to enter room_name in Room Name field
        :return: SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.CONFIRM_DELETE_TEXTBOX).send_keys(text)
        return self

    def enable_bluetooth(self) -> None:
        """
        Method to enable Bluetooth

        :param none
        :return none
        """
        if self.verify_bluetooth_enabled(timeout=1):
            Report.logInfo("Bluetooth already enabled in Sync Portal")
        else:
            Report.logInfo("Enabling Bluetooth in Sync Portal")
            self.look_element(SyncPortalRoomLocators.BLUETOOTH).click()
            if self.verify_element(SyncPortalRoomLocators.BLUETOOTH_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Bluetooth Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal: Bluetooth Updated Message not displayed")

    def disable_bluetooth(self) -> None:
        """
        Method to disable Bluetooth

        :param none
        :return none
        """
        if self.verify_bluetooth_enabled(timeout=1):
            Report.logInfo("Disabling Bluetooth in Sync Portal")
            self.look_element(SyncPortalRoomLocators.BLUETOOTH).click()
            if self.verify_element(SyncPortalRoomLocators.BLUETOOTH_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Bluetooth Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal: Bluetooth Updated Message not displayed")
        else:
            Report.logInfo("Bluetooth already disabled in Sync Portal")

    def enable_speaker_boost(self) -> None:
        """
        Method to enable Speaker Boost

        :param :
        :return :
        """
        if self.verify_speaker_boost_enabled(timeout=1):
            Report.logInfo("Speaker Boost is already enabled in Sync Portal")
        else:
            Report.logInfo("Enabling Speaker Boost in Sync Portal")
            self.look_element(SyncPortalRoomLocators.SPEAKER_BOOST).click()
            if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Settings Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal: Settings Updated Message not displayed")

    def disable_speaker_boost(self) -> None:
        """
        Method to disable Speaker Boost

        :param :
        :return :
        """
        if self.verify_speaker_boost_enabled(timeout=1):
            Report.logInfo("Disabling Speaker Boost in Sync Portal")
            self.look_element(SyncPortalRoomLocators.SPEAKER_BOOST).click()
            if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Settings Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal: Settings Updated Message not displayed")
        else:
            Report.logInfo("Speaker Boost is already disabled in Sync Portal")

    def enable_ai_noise_suppression(self) -> None:
        """
        Method to enable AI Noise Suppression

        :param :
        :return :
        """
        if self.verify_ai_noise_suppression_enabled(timeout=1):
            Report.logInfo("AI Noise Suppression is already enabled in Sync Portal")
        else:
            Report.logInfo("Enabling AI Noise Suppression in Sync Portal")
            self.look_element(SyncPortalRoomLocators.AI_NOISE_SUPPRESSION).click()
            if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Settings Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal: Settings Updated Message not displayed")

    def disable_ai_noise_suppression(self) -> None:
        """
        Method to disable AI Noise Suppression

        :param :
        :return :
        """
        if self.verify_ai_noise_suppression_enabled(timeout=1):
            Report.logInfo("Disabling AI Noise Suppression in Sync Portal")
            self.look_element(SyncPortalRoomLocators.AI_NOISE_SUPPRESSION).click()
            if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Settings Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal: Settings Updated Message not displayed")
        else:
            Report.logInfo("AI Noise Suppression is already disabled in Sync Portal")

    def set_reverb_control_disable(self) -> None:
        """
        Method to set Reverb Control Disable

        :param :
        :return :
        """
        Report.logInfo("Setting Reverb Control Disable in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_DISABLED)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_DISABLED).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def set_reverb_control_normal(self) -> None:
        """
        Method to set Reverb Control Normal

        :param :
        :return :
        """
        Report.logInfo("Setting Reverb Control Normal in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_NORMAL)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_NORMAL).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def set_reverb_control_aggressive(self) -> None:
        """
        Method to set Reverb Control Aggressive

        :param :
        :return :
        """
        Report.logInfo("Setting Reverb Control Aggressive in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_AGGRESSIVE)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_AGGRESSIVE).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def set_microphone_bass_boost(self) -> None:
        """
        Method to set Microphone EQ to Bass Boost

        :param :
        :return :
        """
        Report.logInfo("Setting Microsphone EQ to Bass Boost in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.MICROPHONE_BASS_BOOST)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.MICROPHONE_BASS_BOOST).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def set_microphone_normal(self) -> None:
        """
        Method to set Microphone EQ to Normal - #Sync App Additions

        :param :
        :return :
        """
        Report.logInfo("Setting Microsphone EQ to Normal in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.MICROPHONE_NORMAL)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.MICROPHONE_NORMAL).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def set_microphone_voice_boost(self) -> None:
        """
        Method to set Microphone EQ to Voice Boost

        :param :
        :return :
        """
        Report.logInfo("Setting Microsphone EQ to Voice Boost in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.MICROPHONE_VOICE_BOOST)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.MICROPHONE_VOICE_BOOST).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def set_speaker_bass_boost(self) -> None:
        """
        Method to set Speaker EQ to Bass Boost - #Sync App Additions

        :param :
        :return :
        """
        Report.logInfo("Setting Speaker EQ to Bass Boost in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.SPEAKER_BASS_BOOST)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.SPEAKER_BASS_BOOST).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def set_speaker_normal(self) -> None:
        """
        Method to set Speaker EQ to Normal - #Sync App Additions

        :param :
        :return :
        """
        Report.logInfo("Setting Speaker EQ to Normal in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.SPEAKER_NORMAL)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.SPEAKER_NORMAL).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def set_speaker_voice_boost(self) -> None:
        """
        Method to set Speaker EQ to Voice Boost

        :param :
        :return :
        """
        Report.logInfo("Setting Speaker EQ to Voice Boost in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.SPEAKER_VOICE_BOOST)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.SPEAKER_VOICE_BOOST).click()
        if self.verify_element(SyncPortalRoomLocators.SETTINGS_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")

    def enable_rightsight(self) -> None:
        """
        Method to Enable RightSight in Sync Portal

        :param :
        :return :
        """
        if self.verify_rightsight(enabled=False):
            Report.logInfo("Enabling RightSight in Sync Portal")
            self.look_element(SyncPortalRoomLocators.RIGHTSIGHT).click()
            if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Rightsight Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal:  Rightsight Updated Message not displayed")
        else:
            Report.logInfo("RightSight is already enabled in Sync Portal")

    def disable_rightsight(self) -> None:
        """
        Method to Disable RightSight in Sync Portal

        :param :
        :return :
        """
        if self.verify_rightsight():
            Report.logInfo("Disabling RightSight in Sync Portal")
            self.look_element(SyncPortalRoomLocators.RIGHTSIGHT).click()
            if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Rightsight Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal:  Rightsight Updated Message not displayed")
        else:
            Report.logInfo("RightSight is already disabled in Sync Portal")

    def enable_rightsight2(self) -> None:
        """
        Method to Enable RightSight 2 in Sync Portal

        :param :
        :return :
        """
        if self.verify_rightsight2(enabled=False):
            Report.logInfo("Enabling RightSight 2 in Sync Portal")
            self.look_element(SyncPortalRoomLocators.RIGHTSIGHT2).click()
            if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Rightsight Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal:  Rightsight Updated Message not displayed")
        else:
            Report.logInfo("RightSight 2 is already enabled in Sync Portal")

    def disable_rightsight2(self) -> None:
        """
        Method to Disable RightSight 2 in Sync Portal

        :param :
        :return :
        """
        if self.verify_rightsight2():
            Report.logInfo("Disabling RightSight 2 in Sync Portal")
            self.look_element(SyncPortalRoomLocators.RIGHTSIGHT2).click()
            if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Rightsight Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal:  Rightsight Updated Message not displayed")
        else:
            Report.logInfo("RightSight 2 is already disabled in Sync Portal")

    def set_group_view(self) -> None:
        """
        Method to Set Group View

        :param :
        :return :
        """
        Report.logInfo("Setting Group view in Sync Portal")
        self.look_element(SyncPortalRoomLocators.GROUP_VIEW).click()
        if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Rightsight Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Rightsight Updated Message not displayed")

    def set_speaker_view(self) -> None:
        """
        Method to Set Speaker View

        :param :
        :return :
        """
        Report.logInfo("Setting Speaker view in Sync Portal")
        self.look_element(SyncPortalRoomLocators.SPEAKER_VIEW).click()
        if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Rightsight Updated Message displayed", True)
        else:
            Report.logWarning("Sync Portal:  Rightsight Updated Message not displayed")

    def enable_picture_in_picture(self):
        """
        Method to Enable Picture in Picture in Sync Portal

        :param :
        :return :
        """
        if self.verify_picture_in_picture():
            Report.logInfo("Picture in picture is already enabled in Sync Portal")
        else:
            Report.logInfo("Enabling Picture in picture in Sync Portal")
            self.look_element(SyncPortalRoomLocators.PICTURE_IN_PICTURE).click()
            if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Rightsight Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal:  Rightsight Updated Message not displayed")

    def disable_picture_in_picture(self):
        """
        Method to Disable Picture in Picture in Sync Portal

        :param :
        :return :
        """
        if self.verify_picture_in_picture(enabled=False):
            Report.logInfo("Picture in picture is already disabled in Sync Portal")
        else:
            Report.logInfo("Disabling Picture in picture in Sync Portal")
            self.look_element(SyncPortalRoomLocators.PICTURE_IN_PICTURE).click()
            if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
                Report.logPass("Sync Portal: Rightsight Updated Message displayed", True)
            else:
                Report.logWarning("Sync Portal:  Rightsight Updated Message not displayed")

    def set_speaker_detection_slow(self):
        """
        Method to set Speaker Detection to Slow

        :param :
        :return :
        """
        Report.logInfo("Setting Speaker Detection to Slow in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_SLOW)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_SLOW).click()
        if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")
        sleep(5)

    def set_speaker_detection_default(self):
        """
        Method to set Speaker Detection to Default

        :param :
        :return :
        """
        Report.logInfo("Setting Speaker Detection to Default in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_DEFAULT)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_DEFAULT).click()
        if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")
        sleep(5)

    def set_speaker_detection_fast(self):
        """
        Method to set Speaker Detection to Fast

        :param :
        :return :
        """
        Report.logInfo("Setting Speaker Detection to Fast in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_FAST)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_FAST).click()
        if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")
        sleep(5)

    def set_framing_speed_slow(self):
        """
        Method to set Framing Speed to Slow

        :param :
        :return :
        """
        Report.logInfo("Setting Framing Speed to Slow in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_SLOW)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_SLOW).click()
        if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")
        sleep(5)

    def set_framing_speed_default(self):
        """
        Method to set Framing Speed to Default

        :param :
        :return :
        """
        Report.logInfo("Setting Framing Speed to Default in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_DEFAULT)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_DEFAULT).click()
        if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")
        sleep(5)

    def set_framing_speed_fast(self):
        """
        Method to set Framing Speed to Fast

        :param :
        :return :
        """
        Report.logInfo("Setting Framing Speed to Fast in Sync Portal")
        e = self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_FAST)
        self.click_by_script(e)
        # self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_FAST).click()
        if self.verify_element(SyncPortalRoomLocators.RIGHTSIGHT_SUCCESS_MESSAGE):
            Report.logPass("Sync Portal: Settings Updated Message displayed", True)
        else:
            Report.logFail("Sync Portal:  Settings Updated Message not displayed")
        sleep(5)

    def get_room_provision_code(self) -> str:
        """
        Method to get Room Provision code

        :param :
        :return : str
        """
        try:
            if self.verify_add_collabos_device_displayed():
                self.click_add_collabos_device()
            provision_code = ''
            provision_code_elements = self.look_all_elements(SyncPortalRoomLocators.PROVISION_CODE)
            for code in provision_code_elements:
                provision_code = provision_code + code.text
            return provision_code
        except Exception as e:
            Report.logException(str(e))
            return ''

    def get_menu_item_value(self, item_name: str) -> str:
        """
        Method to get Room Provision code

        :param item_name:str:
        :return : str
        """
        return self.look_element(SyncPortalRoomLocators.MENU_ITEM, param=item_name).text

    def verify_device_exists_in_room(self, device_name: str) -> bool:
        """
        Method to verify device exists in left panel of room

        :param device_name:str:
        :return: bool
        """
        return self.verify_element(SyncPortalRoomLocators.LEFT_NAV_DEVICE, param=device_name, timeunit=5)

    def verify_personal_device_availability_in_personal_device_room(self, device_name: str,
                                                                    is_online: Optional[bool] = None) -> bool:
        """
        Args:
            device_name (str): The name of the device to verify availability.
            is_online (bool, optional): The expected online status of the device. Defaults to None.

        Returns:
            bool: True if the device is found with the expected status within 90 seconds, False otherwise.

        Description:
        This method verifies the availability of a personal device in a personal device room. It checks the device status on the main dashboard, retries if necessary, and returns the result.

        If the device is not found initially, the method will retry every 5 seconds until the device is found or the timeout of 90 seconds is reached.

        If the device is found, the method compares the status of the device with the expected status (is_online). If they are the same, the method logs a success message and returns True. If they are different, the method logs an error message and retries.

        If the timeout is reached and the device is still not found with the expected status, the method logs a timeout message and returns False.

        Note: This method uses the Report class for logging information and taking screenshots.

        Example:
            verify_personal_device_availability_in_personal_device_room(device_name='device1', is_online=True)
        """
        start_time = time()
        Report.logInfo(f'Verify {device_name} status on main dashboard.')
        while time() - start_time < 90:
            device = self._find_personal_device(device_name)
            if device is None:
                Report.logInfo(f"Device {device_name} not found. Retrying...")
                sleep(5)
                continue

            device_status = self._get_personal_device_status(device)

            if device_status is None:
                Report.logInfo(f"Could not get status for device {device_name}. Retrying...")
            elif device_status == is_online:
                Report.logInfo(
                    f"Device {device_name} found with the expected status: '{self.translate_device_status(device_status)}'")
                return True
            else:
                Report.logInfo(
                    f"Device {device_name} found, but with the wrong status: '{self.translate_device_status(device_status)}'. Expected status: '{self.translate_device_status(is_online)}'. Retrying...")

            sleep(5)

        Report.logInfo(f'Time out. Device {device_name} was not found with the expected status within 90 seconds.',
                       screenshot=True)
        return False

    @staticmethod
    def translate_device_status(status: str) -> str:
        """
        Translates the status of a device.

        Args:
            status (str): The status of the device.

        Returns:
            str: The translated status.

        """
        if status == DEVICE_ONLINE_STATUS:
            return "Online"
        elif status == DEVICE_OFFLINE_STATUS:
            return "Offline"
        else:
            return "Unknown"

    def _find_personal_device(self, device_name: str) -> Any:
        """
        Args:
            device_name: The name of the device to be found.

        Returns:
            The found device element if it exists, or None if the device is not found.
        """
        all_devices = self.look_all_elements(
            (By.XPATH, "//a[contains(@class, 'SideNavComponents__StyledNavLink')]"))
        return next((device for device in all_devices if device.text == device_name), None)

    def _get_personal_device_status(self, device: str) -> str:
        """
        Args:
            device: The device element to retrieve the status from.

        Returns:
            The status of the personal device as a string. The status is retrieved from the 'fill' attribute of the child element of the device, which is found using an XPath query.

        Example:
            device = driver.find_element(By.XPATH, "//div[@class='personal-device']")
            status = _get_personal_device_status(device)
        """
        child_element = device.find_element(By.XPATH, "./*[name()='svg']/*[name()='g']")
        return child_element.get_attribute('fill')

    def _report_personal_device_status(self, device_name: str, expected_status: str, actual_status: str) -> bool:
        if actual_status == expected_status:
            Report.logPass(f"Device {device_name} is displayed and status is as expected.")
            return True
        else:
            Report.logFail(f"Device {device_name} is displayed but showing wrong status.")
            return False

    def verify_anti_flicker_ntsc_selected(self, timeout: int = 15) -> bool:
        """
        Method to Verify Anti flicker setting NTSC Enabled

        :param timeout:
        :return bool
        """
        while timeout > 0:
            if self.look_element(SyncPortalRoomLocators.NTSC_60HZ).is_selected():
                break
            sleep(1)
            timeout -= 1
        return self.look_element(SyncPortalRoomLocators.NTSC_60HZ).is_selected()

    def verify_anti_flicker_pal_selected(self, timeout: int = 15) -> bool:
        """
        Method to Verify Anti flicker setting PAL Enabled

        :param timeout:
        :return bool
        """
        while timeout > 0:
            if self.look_element(SyncPortalRoomLocators.PAL_50HZ).is_selected():
                break
            sleep(1)
            timeout -= 1
        return self.look_element(SyncPortalRoomLocators.PAL_50HZ).is_selected()

    def verify_bluetooth_enabled(self, timeout: int = 15) -> bool:
        """
        Method to Verify Bluetooth Enabled

        :param timeout:
        :return bool
        """
        while timeout > 0:
            e = self.look_element(SyncPortalRoomLocators.BLUETOOTH_STATUS)
            if e.get_attribute('fill') == '#814efa':
                return True
            sleep(1)
            timeout -= 1
        return False

    def verify_speaker_boost_enabled(self, timeout: int = 15) -> bool:
        """
        Method to Verify Speaker Boost Enabled

        :param timeout:
        :return bool
        """
        while timeout > 0:
            e = self.look_element(SyncPortalRoomLocators.SPEAKER_BOOST_STATUS)
            if e.get_attribute('fill') == '#814efa':
                return True
            sleep(1)
            timeout -= 1
        return False

    def verify_ai_noise_suppression_enabled(self, timeout: int = 15) -> bool:
        """
        Method to Verify AI Noise Suppression Enabled

        :param timeout:
        :return bool
        """
        while timeout > 0:
            e = self.look_element(SyncPortalRoomLocators.AI_NOISE_SUPPRESSION_STATUS)
            if e.get_attribute('fill') == '#814efa':
                return True
            sleep(1)
            timeout -= 1
        return False

    def verify_reverb_control_disable_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Reverb Control Disable is selected

        :param :
        :return bool:
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_DISABLED)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_reverb_control_normal_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Reverb Control Normal is selected

        :param :
        :return bool:
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_NORMAL)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_reverb_control_aggressive_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Reverb Control Aggressive is selected

        :param :
        :return bool:
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.REVERB_CONTROL_AGGRESSIVE)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_microphone_bass_boost_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Microphone EQ Bass Boost is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.MICROPHONE_BASS_BOOST)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_microphone_normal_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Microphone EQ Normal is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.MICROPHONE_NORMAL)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_microphone_voice_boost_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Microphone EQ Voice Boost is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.MICROPHONE_VOICE_BOOST)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_speaker_bass_boost_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Speaker EQ Bass Boost is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.SPEAKER_BASS_BOOST)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_speaker_normal_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Speaker EQ Normal is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.SPEAKER_NORMAL)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_speaker_voice_boost_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Speaker EQ Voice Boost is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.SPEAKER_VOICE_BOOST)
            if e.is_selected():
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_device_forget_message(self) -> bool:
        """
        Method to Verify device forget message displayed

        :param :
        :return :
        """
        return self.verify_element(SyncPortalRoomLocators.DEVICE_FORGET_MESSAGE)

    def verify_group_view_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Group View selected

        :param refresh_count:
        :return bool:
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.GROUP_VIEW)
            if str(e.get_attribute('class')).__contains__('hwMrgr'):
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_speaker_view_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Speaker View selected

        :param refresh_count:
        :return bool:
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.SPEAKER_VIEW)
            if str(e.get_attribute('class')).__contains__('hwMrgr'):
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_picture_in_picture(self, refresh_count: int = 1, enabled: bool = True) -> bool:
        """
        Method to Verify Picture In Picture Enabled

        :param refresh_count:
        :return bool
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.PICTURE_IN_PICTURE_STATUS)
            if enabled and e.get_attribute('fill') == '#814efa':
                return True
            elif not enabled and e.get_attribute('fill') != '#814efa':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_rightsight(self, refresh_count: int = 1, enabled: bool = True) -> bool:
        """
        Method to Verify RightSight Enabled

        :param enabled:
        :param refresh_count:
        :return bool
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.RIGHTSIGHT_STATUS)
            if enabled and e.get_attribute('fill') == '#814efa':
                return True
            if not enabled and e.get_attribute('fill') != '#814efa':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_rightsight2(self, refresh_count: int = 1, enabled: bool = True) -> bool:
        """
        Method to Verify RightSight Enabled

        :param enabled:
        :param refresh_count:
        :return bool
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.RIGHTSIGHT2_STATUS)
            if enabled and e.get_attribute('fill') == '#814efa':
                return True
            if not enabled and e.get_attribute('fill') != '#814efa':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_speaker_detection_slow_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Speaker Detection Slow is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_SLOW)
            if e.get_attribute('value') == 'true':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_speaker_detection_default_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Speaker Detection Default is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_DEFAULT)
            if e.get_attribute('value') == 'true':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_speaker_detection_fast_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Speaker Detection Fast is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.SPEAKER_DETECTION_FAST)
            if e.get_attribute('value') == 'true':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_framing_speed_slow_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Framing Speed Slow is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_SLOW)
            if e.get_attribute('value') == 'true':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_framing_speed_default_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Framing Speed Default is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_DEFAULT)
            if e.get_attribute('value') == 'true':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_framing_speed_fast_selected(self, refresh_count: int = 1) -> bool:
        """
        Method to Verify Framing Speed Fast is selected

        :param refresh_count:
        :return :
        """
        while refresh_count > 0:
            e = self.look_element(SyncPortalRoomLocators.FRAMING_SPEED_FAST)
            if e.get_attribute('value') == 'true':
                return True
            global_variables.driver.refresh()
            sleep(5)
            refresh_count -= 1
        return False

    def verify_firmware_update_available(self) -> bool:
        """
        Method to verify firmware update available for a device connected to room

        :param :
        :return : bool
        """
        return self.verify_element(SyncPortalRoomLocators.FIRMWARE_UPDATE_AVAILABLE)

    def verify_room_deleted_message(self) -> bool:
        """
        Method to verify Room deleted message

        :param :
        :return :bool
        """
        return self.verify_element(SyncPortalRoomLocators.DELETE_SUCCESS_MESSAGE)

    def verify_swytch_connected_to_external_pc_message_displayed(self, displayed: bool = True) -> bool:
        """
        Method to Verify Swytch status when Swycth connected to Guest PC- #Sync App Additions

        :param displayed:
        :return :bool
        """
        refresh_count = 5
        while refresh_count > 0:
            if displayed and self.verify_element(SyncPortalRoomLocators.SWYTCH_CONNECTED_TO_EXTERNAL_PC, timeunit=2):
                return True
            elif not displayed and not self.verify_element(SyncPortalRoomLocators.SWYTCH_CONNECTED_TO_EXTERNAL_PC,
                                                           timeunit=2):
                return True
            else:
                sleep(5)
                global_variables.driver.refresh()
                refresh_count -= 1
        return False

    def verify_swytch_byod_device_status_message_displayed(self, displayed: bool = True) -> bool:
        """
        Method to Verify device status when Swycth connected to Guest PC- #Sync App Additions

        :param displayed:
        :return bool:
        """
        refresh_count = 5
        while refresh_count > 0:
            if displayed and self.verify_element(SyncPortalRoomLocators.SWYTCH_BYOD_DEVICE_STATUS, timeunit=2):
                True
            elif not displayed and not self.verify_element(SyncPortalRoomLocators.SWYTCH_BYOD_DEVICE_STATUS,
                                                           timeunit=2):
                True
            else:
                sleep(5)
                global_variables.driver.refresh()
                refresh_count -= 1
        return False

    def verify_swytch_byod_device_settings_message_displayed(self, displayed: bool = True) -> bool:
        """
        Method to Verify device settings when Swycth connected to Guest PC- #Sync App Additions

        :param displayed:
        :return bool:
        """
        refresh_count = 5
        while refresh_count > 0:
            if displayed and self.verify_element(SyncPortalRoomLocators.SWYTCH_BYOD_DEVICE_SETTINGS, timeunit=2):
                break
            elif not displayed and not self.verify_element(SyncPortalRoomLocators.SWYTCH_BYOD_DEVICE_SETTINGS,
                                                           timeunit=2):
                break
            else:
                sleep(5)
                global_variables.driver.refresh()
                refresh_count -= 1
        return False

    def click_close_button(self):
        """
        Method to click on Close button to exit Room view

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.CLOSE_BUTTON).click()
        return self

    def verify_add_collabos_device_displayed(self) -> bool:
        """
        Method to Verify Add CollabOS device option displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncPortalRoomLocators.ADD_COLLABOS_DEVICE, timeunit=10)

    def click_add_collabos_device(self):
        """
        Method to click on Add CollabOS device

        :param :
        :return : SyncPortalRoom
        """
        self.look_element(SyncPortalRoomLocators.ADD_COLLABOS_DEVICE).click()
        return self
