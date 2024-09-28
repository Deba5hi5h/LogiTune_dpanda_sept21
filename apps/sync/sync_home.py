import time

from selenium.webdriver.common.keys import Keys

from apps.sync.sync_app import SyncApp
from apps.sync.sync_device import SyncDevice
from apps.sync.sync_device_audio import SyncDeviceAudio
from apps.sync.sync_device_camera import SyncDeviceCamera
from apps.sync.sync_device_connectivity import SyncDeviceConnectivity
from apps.sync.sync_room import SyncRoom
from base import global_variables
from base.base_ui import UIBase
from locators.sync_app.sync_app_home_locators import SyncAppHomeLocators


class SyncHome(SyncApp):

    def click_menu(self):
        """
        Method to click on Menu

        :param :
        :return :
        """
        UIBase.elementName = "Menu"
        self.look_element(SyncAppHomeLocators.MENU).click()
        time.sleep(1)
        return SyncHome()

    def click_rename_room(self):
        """
        Method to click on Rename Room menu item

        :param :
        :return SyncHome:
        """
        self.look_element(SyncAppHomeLocators.RENAME_ROOM).click()
        time.sleep(1)
        return SyncHome()

    def click_room(self) -> SyncRoom:
        """
        Method to click on Room

        :param :
        :return SyncRoom:
        """
        e = self.look_element(SyncAppHomeLocators.ROOM)
        self.click_by_script(e)
        return SyncRoom()

    def click_device(self, device_name) -> SyncDevice:
        """
        Method to click on device from left navigation

        :param device_name: E.g. Rally Bar
        :return SyncDeviceAudio:
        """
        e = self.look_element(SyncAppHomeLocators.DEVICE_NAME, param=device_name)
        self.click_by_script(e)
        time.sleep(2)
        return SyncDevice()

    def click_device_audio(self, device_name) -> SyncDeviceAudio:
        """
        Method to click on Audio section for device

        :param device_name: E.g. Rally Bar
        :return SyncDeviceAudio:
        """
        e = self.look_element(SyncAppHomeLocators.DEVICE_AUDIO, param=device_name)
        self.click_by_script(e)
        time.sleep(2)
        return SyncDeviceAudio()

    def click_device_camera(self, device_name) -> SyncDeviceCamera:
        """
        Method to click on Camera section for device

        :param device_name: E.g. Rally Bar
        :return SyncDeviceCamera:
        """
        e = self.look_element(SyncAppHomeLocators.DEVICE_CAMERA, param=device_name)
        self.click_by_script(e)
        time.sleep(5)
        return SyncDeviceCamera()

    def click_device_connectivity(self, device_name) -> SyncDeviceConnectivity:
        """
        Method to click on Connectivity section for device

        :param device_name: E.g. Rally Bar
        :return SyncDeviceConnectivity:
        """
        e = self.look_element(SyncAppHomeLocators.DEVICE_CONNECTIVITY, param=device_name)
        self.click_by_script(e)
        return SyncDeviceConnectivity()

    def click_add_device(self):
        """
        Method to click on add device (+) icon

        :param :
        :return SyncHome:
        """
        self.look_element(SyncAppHomeLocators.ADD_DEVICE).click()
        return SyncHome()

    def click_updates_and_about(self):
        """
        Method to click Updates and About menu item

        :param :
        :return :
        """
        self.look_element(SyncAppHomeLocators.UPDATES_AND_ABOUT, wait_for_visibility=True).click()
        return SyncHome()

    def click_about_logitech_sync(self):
        """
        Method to click About Logitech Sync menu item

        :param :
        :return :
        """
        self.look_element(SyncAppHomeLocators.ABOUT_LOGITECH_SYNC, wait_for_visibility=True).click()
        return SyncHome()

    def click_check_for_update(self):
        """
        Method to click Check for Update link

        :param :
        :return :
        """
        self.look_element(SyncAppHomeLocators.CHECK_FOR_UPDATE, wait_for_visibility=True).click()
        self.verify_element(SyncAppHomeLocators.ROOM_SYNC_UPDATE, timeunit=10)
        return SyncHome()

    def click_sync_update_now(self) -> None:
        """
        Method to click Update Now from Sync update screen

        :param None
        :return None
        """
        self.look_element(SyncAppHomeLocators.UPDATE_NOW, wait_for_visibility=True).click()

    def type_in_room_edit_box(self, input_text: str):
        """
        Method to input in room edit box

        :param input_text:
        :return SyncHome:
        """
        room_edit = self.look_element(SyncAppHomeLocators.ROOM_EDIT_BOX)
        time.sleep(1)
        global_variables.driver.execute_script("arguments[0].value=''", room_edit)
        room_edit.send_keys(input_text + Keys.ENTER)
        return SyncHome()

    def get_room_name(self) -> str:
        """
        Method to Rename Room

        :param :
        :return str:
        """
        e = self.look_element(SyncAppHomeLocators.ROOM_NAME, wait_for_visibility=True)
        return e.text

    def verify_device_displayed(self, device_name: str) -> bool:
        """
        Method to verify device displayed in left navigation

        :param device_name:
        :return bool:
        """
        return self.verify_element(SyncAppHomeLocators.DEVICE_NAME, 5, param=device_name)

    @staticmethod
    def get_number_of_nodes() -> int:
        """
        Method to count the number of Nodes displayed on the left panel of Sync App

        :param :
        :return count: int
        """
        list_of_nodes = global_variables.driver.find_elements(*SyncAppHomeLocators.UI_NODES)
        return len(list_of_nodes)
