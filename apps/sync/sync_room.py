import time

from selenium.webdriver.common.keys import Keys

from apps.sync.sync_app import SyncApp
from apps.sync.sync_device_audio import SyncDeviceAudio
from base import global_variables
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_app.sync_app_room_locators import SyncAppRoomLocators


class SyncRoom(SyncApp):

    def click_info(self):
        """
        Method to click on info icon in Sync App

        :param :
        :return SyncRoom:
        """
        UIBase.elementName = "Info"
        self.look_element(SyncAppRoomLocators.ROOM_INFO).click()
        return SyncRoom()

    def click_connect_to_sync_portal(self):
        """
        Method to click on Connect to Sync Portal link

        :param :
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.CONNECT_TO_SYNC_PORTAL, wait_for_visibility=True).click()
        return SyncRoom()

    def click_disconnect_room(self):
        """
        Method to click on Disconnect Room link

        :param :
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.DISCONNECT_ROOM).click()
        return SyncRoom()

    def click_email_and_password(self):
        """
        Method to click on Email and Password link

        :param :
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.EMAIL_SETUP).click()
        time.sleep(2)
        return SyncRoom()

    def click_room_provision_code(self):
        """
        Method to click on Room provision codelink

        :param :
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.PROVISION_CODE_SETUP).click()
        time.sleep(2)
        return SyncRoom()

    def click_connect_room(self):
        """
        Method to click on Connect Room button

        :param :
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.CONNECT_ROOM).click()
        return SyncRoom()

    def click_join(self):
        """
        Method to click on Join button

        :param :
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.JOIN).click()
        return SyncRoom()

    def click_ok(self):
        """
        Method to click on OK button

        :param :
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.OK_BUTTON).click()
        return SyncRoom()

    def click_update(self):
        """
        Method to click Update from Room screen

        :param :
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.ROOM_SYNC_UPDATE).click()
        return SyncRoom()

    def select_org_name(self, org_name: str):
        """
        Method to select Organization Name radio button

        :param org_name:
        :return SyncRoom:
        """
        try:
            self.look_element(SyncAppRoomLocators.ORG_NAME, param=org_name).click()
        except:
            Report.logInfo(f"Unable to select {org_name}")
        return SyncRoom()

    def type_in_user_name(self, input_text: str):
        """
        Method to input text in User Name field

        :param input_text:
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.USER_NAME).send_keys(input_text)
        return SyncRoom()

    def type_in_password(self, input_text: str):
        """
        Method to input text in Password field

        :param input_text:
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.PASSWORD).send_keys(input_text)
        return SyncRoom()

    def type_in_provision_code(self, input_text: str):
        """
        Method to input text in User Name field

        :param input_text:
        :return SyncRoom:
        """
        self.look_element(SyncAppRoomLocators.PROVISION_CODE).send_keys(input_text)
        return SyncRoom()

    def type_in_seat_count(self, input_text: str):
        """
        Method to input text in Seat Count field

        :param input_text:
        :return SyncRoom:
        """
        seat_edit = self.look_element(SyncAppRoomLocators.SEAT_COUNT, wait_for_visibility=True)
        time.sleep(1)
        global_variables.driver.execute_script("arguments[0].value=''", seat_edit)
        seat_edit.send_keys(input_text + Keys.ENTER)
        return SyncRoom()

    def get_computer_type(self) -> str:
        """
        Method to get Computer Type displayed in Room Information

        :param :
        :return str:
        """
        return self.look_element(SyncAppRoomLocators.COMPUTER_TYPE).text

    def get_operating_system(self) -> str:
        """
        Method to get Operating System displayed in Room Information

        :param :
        :return str:
        """
        return self.look_element(SyncAppRoomLocators.OPERATING_SYSTEM).text

    def get_os_version(self) -> str:
        """
        Method to get OS Version displayed in Room Information

        :param :
        :return str:
        """
        return self.look_element(SyncAppRoomLocators.OS_VERSION).text

    def get_processor(self) -> str:
        """
        Method to get Processor displayed in Room Information

        :param :
        :return str:
        """
        return self.look_element(SyncAppRoomLocators.PROCESSOR).text

    def get_memory(self) -> str:
        """
        Method to get Memory displayed in Room Information

        :param :
        :return str:
        """
        return self.look_element(SyncAppRoomLocators.MEMORY).text

    def verify_connect_button_enabled(self) -> bool:
        """
        Method to verify Connect button is enabled

        :param :
        :return bool:
        """
        return self.look_element(SyncAppRoomLocators.CONNECT_ROOM).is_enabled()

    def verify_room_connected(self) -> bool:
        """
        Method to verify Room is connected to Sync Portal

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppRoomLocators.ROOM_CONNECTED)

    def verify_room_disconnected(self) -> bool:
        """
        Method to verify Room is connected to Sync Portal

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppRoomLocators.CONNECT_TO_SYNC_PORTAL, wait_for_visibility=True)

    def verify_org_name_selected(self, org_name: str) -> bool:
        """
        Method to verify Room is connected to Sync Portal

        :param org_name:
        :return bool:
        """
        return self.look_element(SyncAppRoomLocators.GROUP_RADIO, org_name).is_selected()

    def verify_no_org_name_associated(self) -> bool:
        """
        Method to verify No Organization is associated message displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppRoomLocators.NO_ORGANIZATION_MSG, wait_for_visibility=True)

    def verify_third_party_permission(self) -> bool:
        """
        Method to verify Third Party permission message displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppRoomLocators.THIRD_PARTY_MSG, wait_for_visibility=True)

    def verify_no_permission_to_disconnect(self) -> bool:
        """
        Method to verify message Please contact an admin with permission to add rooms.

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppRoomLocators.DISCONNECT_PERMISSION_MSG, wait_for_visibility=True)

    def verify_multiple_hosts_code_error(self) -> bool:
        """
        Method to verify message This room already has host PC/appliance device.

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppRoomLocators.PROVISION_CODE_MULTIPLE_HOSTS_ERROR, wait_for_visibility=True)

    def verify_incorrect_code_error(self) -> bool:
        """
        Method to verify message This provisioning code is invalid.

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppRoomLocators.INCORRECT_PROVISION_CODE_ERROR, wait_for_visibility=True)

    def verify_new_sync_version_available_banner(self) -> bool:
        """
        Method to verify New Sync App version available banner in Room

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppRoomLocators.ROOM_SYNC_UPDATE_AVAILABLE, timeunit=10)