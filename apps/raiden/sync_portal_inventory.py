import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from apps.raiden.sync_portal_room import SyncPortalRoom
from base import global_variables, base_settings
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_portal.sync_portal_inventory_locators import SyncPortalInventoryLocators


class SyncPortalInventory(UIBase):
    """
    Sync Portal Inventory Page test methods
    """
    def search(self, search_text: str):
        """
        Method to search in Inventory Page
        :return: SyncPortalInventory
        """
        self.look_element(SyncPortalInventoryLocators.SEARCH_BOX).clear()
        self.look_element(SyncPortalInventoryLocators.SEARCH_BOX).send_keys(search_text)
        time.sleep(2)
        return SyncPortalInventory()

    def click_on_add_room(self):
        """
        Method to Click on Add Room in Inventory Page
        :return: SyncPortalInventory
        """
        self.look_element(SyncPortalInventoryLocators.ADD_ROOM).click()
        return SyncPortalInventory()

    def click_on_empty_room(self):
        """
        Method to Click on Empty Room
        :return: SyncPortalInventory
        """
        self.look_element(SyncPortalInventoryLocators.EMPTY_ROOM).click()
        return SyncPortalInventory()

    def click_on_create_button(self):
        """
        Method to Click on Create button
        :return: SyncPortalInventory
        """
        WebDriverWait(global_variables.driver, 5).until(
            expected_conditions.element_to_be_clickable(SyncPortalInventoryLocators.CREATE_BUTTON))
        self.look_element(SyncPortalInventoryLocators.CREATE_BUTTON).click()
        return SyncPortalInventory()

    def click_on_inventory_room(self, room_name: str, timeunit: int = base_settings.IMPLICIT_WAIT) -> SyncPortalRoom:
        """
        Method to Click on Room name in Inventory Page
        :return: SyncPortalRoom
        """
        self.look_element(SyncPortalInventoryLocators.INVENTORY_ROOM, param=room_name).click()
        self.verify_element(SyncPortalInventoryLocators.LEFT_NAVIGATION_ROOM, timeunit=timeunit)
        return SyncPortalRoom()

    def click_on_devices_tab(self) -> None:
        """
        Method to Click on Room name in Inventory Page
        :return: SyncPortalRoom
        """
        self.look_element(SyncPortalInventoryLocators.DEVICES_TAB).click()

    def type_in_create_room_name(self, room_name: str):
        """
        Method to enter room_name in Room Name field
        :return: SyncPortalInventory
        """
        self.look_element(SyncPortalInventoryLocators.CREATE_ROOM_NAME).send_keys(room_name)
        return SyncPortalInventory()

    def type_in_create_room_seat(self, seat_count: str):
        """
        Method to enter seat_count in Seat Count field
        :return: SyncPortalInventory
        """
        self.look_element(SyncPortalInventoryLocators.CREATE_ROOM_SEAT).send_keys(seat_count)
        return SyncPortalInventory()

    def get_list_of_devices_in_room(self, room_name: str):
        """
        Method to get list of devices connected to room

        :param room_name:str:
        :return list of devices:list:
        """
        try:
            self.search(search_text=room_name)
            devices_cell = self.look_element(SyncPortalInventoryLocators.ROOM_DEVICES, room_name)
            self.highLightElement(devices_cell)
            device_list = list(str(devices_cell.text).split(','))
            res = list(map(str.strip, device_list))
            return res
        except Exception as e:
            Report.logException(str(e))
            raise e

    def verify_personal_room_is_created(self, room_name: str) -> list:
        """
        Method to get list of devices connected to room

        :param room_name:str:
        :return list of devices:list:
        """
        try:
            self.search(search_text=room_name)
            room = self.look_element(SyncPortalInventoryLocators.ROOM_DEVICES, room_name)
            devices_cell = self.look_element(SyncPortalInventoryLocators.ROOM_DEVICES, room_name)
            self.highLightElement(devices_cell)
            device_list = list(str(devices_cell.text).split(','))
            res = list(map(str.strip, device_list))
            return res
        except Exception as e:
            Report.logException(str(e))
            raise e


    def get_room_status(self, room_name: str) -> str:
        """Returns the status of a given room.

        Args:
            room_name (str): The name of the room.

        Returns:
            str: The status of the room.
        """
        room_status = self.look_element(SyncPortalInventoryLocators.ROOM_STATUS, param=room_name)
        return room_status.text

    def get_room_health(self, room_name) -> str:
        """
        Method to get room health displayed in Inventory Page
        :param room_name
        :return str
        """
        room_health = self.look_element(SyncPortalInventoryLocators.ROOM_HEALTH, param=room_name)
        return room_health.text

    def get_room_use_state(self, room_name) -> str:
        """
        Method to get room Use State displayed in Inventory Page
        :param room_name
        :return str
        """
        room_use_state = self.look_element(SyncPortalInventoryLocators.ROOM_USE_STATE, param=room_name)
        return room_use_state.text

    def get_device_status(self, device_name) -> str:
        """
        Method to get device status displayed in Inventory Devices tab
        :param device_name
        :return str
        """
        device_status = self.look_element(SyncPortalInventoryLocators.DEVICE_STATUS, param=device_name)
        return device_status.text

    def get_device_health(self, device_name) -> str:
        """
        Method to get device health displayed in Inventory Devices tab
        :param device_name
        :return str
        """
        device_status = self.look_element(SyncPortalInventoryLocators.DEVICE_HEALTH, param=device_name)
        return device_status.text

    def get_device_use_state(self, device_name) -> str:
        """
        Method to get device use state displayed in Inventory Devices tab
        :param device_name
        :return str
        """
        device_status = self.look_element(SyncPortalInventoryLocators.DEVICE_USE_STATE, param=device_name)
        return device_status.text

    def verify_room_displayed_in_inventory(self, room_name: str, timeunit: int = 2) -> bool:
        """
        Method to verify room status displayed correctly in Inventory Page
        :param room_name
        : param timeunit:int
        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.INVENTORY_ROOM, param=room_name, timeunit=timeunit)

    def verify_room_header_displayed(self) -> bool:
        """
        Method to verify room header displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.ROOM_HEADER, timeunit=10)

    def verify_group_header_displayed(self) -> bool:
        """
        Method to verify Group header displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.GROUP_HEADER, timeunit=2)

    def verify_device_header_displayed(self) -> bool:
        """
        Method to verify Device header displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.DEVICES_HEADER, timeunit=2)

    def verify_devices_header_displayed(self) -> bool:
        """
        Method to verify Devices header displayed in Inventory Page (Devices)

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.DEVICES_HEADER, timeunit=2)

    def verify_sync_version_header_displayed(self) -> bool:
        """
        Method to verify Sync Version header displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.SYNC_VERSION_HEADER, timeunit=2)

    def verify_version_header_displayed(self) -> bool:
        """
        Method to verify Version header displayed in Inventory Page (Devices)

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.VERSION_HEADER, timeunit=2)

    def verify_status_header_displayed(self) -> bool:
        """
        Method to verify Status header displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.STATUS_HEADER, timeunit=2)

    def verify_health_header_displayed(self) -> bool:
        """
        Method to verify Health header displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.HEALTH_HEADER, timeunit=2)

    def verify_use_state_header_displayed(self) -> bool:
        """
        Method to verify Use State header displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.USE_STATE_HEADER, timeunit=2)

    def verify_seat_count_header_displayed(self) -> bool:
        """
        Method to verify Seat Count header displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.SEAT_COUNT_HEADER, timeunit=2)

    def verify_room_status_displayed(self, room_name, status) -> bool:
        """
        Method to verify room status displayed correctly in Inventory Page
        :param room_name
        :param status
        :return bool
        """
        room_status = self.look_element(SyncPortalInventoryLocators.ROOM_STATUS, param=room_name)
        self.highLightElement(room_status)
        if room_status.text == status:
            return True
        else:
            return False

    def verify_room_created_message(self) -> bool:
        """
        Method to verify Room created successfully message in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.CREATE_ROOM_SUCCESS_MSG)

    def verify_search_box_displayed(self) -> bool:
        """
        Method to verify Search Box displayed in Inventory Page

        :return bool
        """
        return self.verify_element(SyncPortalInventoryLocators.SEARCH_BOX, timeunit=5)