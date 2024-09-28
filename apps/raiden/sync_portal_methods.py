import time

from apps.browser_methods import BrowserClass
from apps.raiden.sync_portal_home import SyncPortalHome
from apps.raiden.sync_portal_inventory import SyncPortalInventory
from apps.raiden.sync_portal_login import SyncPortalLogin
from apps.raiden.sync_portal_room import SyncPortalRoom
from apps.raiden.sync_portal_users import SyncPortalUsers
from base import global_variables
from base.base_ui import UIBase
from extentreport.report import Report


class SyncPortalMethods(UIBase):
    """
    Sync Portal test methods
    """

    browser = BrowserClass()
    inventory = SyncPortalInventory()
    room = SyncPortalRoom()
    home = SyncPortalHome()

    def login_to_sync_portal(self, config: str, role: str) -> SyncPortalInventory:
        """
        Method to Login to Sync Portal

        :param role: Sync Portal user role
        :param config: Config object downloaded from AWS
        :return:
        """
        self.browser.open_browser(global_variables.config.BASE_URL)
        if global_variables.ENABLE_PROXY:
            self.browser.refresh()
        return SyncPortalLogin().login(config=config, role=role)

    def login_to_sync_portal_personal_devices(self, config: str, role: str) -> SyncPortalInventory:
        """
        Method to Login to Sync Portal

        :param role: Sync Portal user role
        :param config: Config object downloaded from AWS
        :return:
        """
        self.browser.open_browser("https://sync.logitech.com/personal/inventory/hzlvTkSj3ax9EXZubDHaAT12f127ersX/computers")
        return SyncPortalLogin().login(config=config, role=role)

    def login_to_sync_portal_and_open_room(self, config: str, role: str, room_name: str) -> None:
        """
        Method to Login to Sync Portal and open the room

        :param role: Sync Portal user role
        :param config: Config object downloaded from AWS
        :param room_name: Sync Portal Room to be opened
        :return:
        """
        return self.login_to_sync_portal(config=config, role=role) \
            .search(search_text=room_name) \
            .click_on_inventory_room(room_name=room_name)

    def login_to_sync_portal_and_create_empty_room(self, config: str, role: str, room_name: str, seat_count: int):
        """
        Method to Login to Sync Portal and Create empty room

        :param seat_count:
        :param role: Sync Portal user role
        :param config: Config object downloaded from AWS
        :param room_name: Sync Portal Room to be opened
        :return:
        """
        inventory = self.login_to_sync_portal(config=config, role=role) \
            .search(search_text=room_name) \
            .click_on_add_room().click_on_empty_room() \
            .type_in_create_room_name(room_name=room_name) \
            .type_in_create_room_seat(seat_count=seat_count) \
            .click_on_create_button()
        if inventory.verify_room_created_message():
            Report.logPass(f'Empty room {room_name} created successfully')
        else:
            Report.logFail(f'Failed to create Empty room {room_name}')
        return inventory

    def verify_room_displayed_in_inventory_search(self, room_name: str) -> bool:
        """
        Method to verify room displayed in inventory search

        :param room_name: Sync Portal Room to be opened
        :return: bool
        """
        inventory = SyncPortalInventory()
        return inventory.search(search_text=room_name).verify_room_displayed_in_inventory(room_name=room_name)

    def login_to_sync_portal_and_verify_provisioned_room(self, config: str, role: str, room_name: str,
                                                         delete_status: bool = False) -> bool:
        """
        Method to Login to Sync Portal and search for provisioned room

        :param delete_status:
        :param room_name:
        :param role: Sync Portal user role
        :param config: Config object downloaded from AWS
        :return:
        """
        inventory = self.login_to_sync_portal(config=config, role=role)
        room_status = inventory.search(search_text=room_name).verify_room_displayed_in_inventory(room_name=room_name)
        refresh_count = 12
        while refresh_count > 0:
            if delete_status and not room_status:
                return True
            elif not delete_status and room_status:
                return True
            else:
                time.sleep(5)
                self.browser.refresh()
                refresh_count -= 1
                room_status = inventory.search(search_text=room_name) \
                    .verify_room_displayed_in_inventory(room_name=room_name)
        return False

    def delete_room(self, room_name: str):
        """
        Method to delete room from Sync Portal

        :param room_name:
        :return:
        """
        room = SyncPortalRoom()
        if room.select_room_checkbox(room_name=room_name).click_delete_button() \
                .type_in_confirm_delete_textbox(
            "Delete").click_confirm_delete_yes_button().verify_room_deleted_message():
            Report.logPass("Room Deleted Successfully", True)
        else:
            Report.logFail("Room not deleted")

    def login_to_sync_portal_and_delete_room(self, config: str, role: str, room_name: str):
        """
        Method to Login to Sync Portal and search for provisioned room

        :param room_name:
        :param role: Sync Portal user role
        :param config: Config object downloaded from AWS
        :return:
        """
        inventory = self.login_to_sync_portal(config=config, role=role)
        room_status = inventory.search(search_text=room_name).verify_room_displayed_in_inventory(room_name=room_name)
        refresh_count = 12
        while refresh_count > 0:
            if room_status:
                break
            else:
                time.sleep(5)
                self.browser.refresh()
                refresh_count -= 1
                room_status = inventory.search(search_text=room_name) \
                    .verify_room_displayed_in_inventory(room_name=room_name)
        self.delete_room(room_name=room_name)
        self.browser.close_browser()

    def change_org(self, org_name: str):
        """
        Method to change organization

        :param org_name:
        :return:
        """
        home = SyncPortalHome()
        home.click_org_selector_icon().click_org_view_all().click_on_org_name(org_name=org_name)

    def change_user_role(self, user: str, role: str):
        """
        Method to change user role

        :param role:
        :param user:
        :return:
        """
        home = SyncPortalHome()
        home.click_system().click_users_tab().type_in_search(search_text=user) \
            .click_on_search_result(search_result=user).click_on_change_role().click_on_role_dropdown() \
            .select_role(role=role).click_save()
        time.sleep(1)

    def change_end_user_group(self, user: str, group: str):
        """
        Method to change user group

        :param group: (user group string separated by comma if multiple groups)
        :param user:
        :return:
        """
        home = SyncPortalHome()
        users = SyncPortalUsers()
        home.click_system().click_users_tab().click_on_end_users().type_in_search(search_text=user)
        time.sleep(2)
        users.click_on_user_checkbox(user=user)
        users.click_on_modify_groups()
        time.sleep(2)
        groups = users.get_current_user_groups_for_user()
        current_groups = groups.split(",")
        # users.click_on_user_group_dropdown()
        for current_group in current_groups:
            users.click_on_user_group_dropdown()
            users.click_on_user_group_selection(user_group=current_group.strip())
        new_groups = group.split(",")
        for new_group in new_groups:
            users.click_on_user_group_dropdown()
            users.click_on_user_group_selection(user_group=new_group.strip())
        time.sleep(2)
        # users.click_on_user_group_dropdown()
        users.click_on_confirm()
        users.verify_user_group_updated_message()
        return groups

    def get_active_end_user_groups(self):
        """
        Method to get active end user groups

        :param :
        :return:
        """
        home = SyncPortalHome()
        users = SyncPortalUsers()
        home.click_system().click_users_tab().click_on_end_users()
        time.sleep(2)
        users.click_on_user_groups_main_screen()
        user_groups = users.get_current_user_groups_added()
        active_user_groups = []
        for group in user_groups:
            if users.get_user_count_for_user_group(user_group=group) > 0:
                active_user_groups.append(group)
        users.click_apply()
        time.sleep(2)
        return active_user_groups

    def logout_from_sync_portal(self) -> bool:
        """
        Method to Logout from Sync Portal

        :param:
        :return bool:
        """
        self.home.click_logout_icon()
        if not self.home.verify_logout():
            self.home.click_logout_icon()
        return self.home.click_logout().verify_login_page()

    @staticmethod
    def report_displayed_or_not(attribute: str, verification: bool, displayed: bool = True,
                                screenshot: bool = True, warning: bool = False):
        value = " " if displayed else " not "
        fail = " not " if displayed else " "
        if verification:
            Report.logPass(f"{attribute}{value}displayed", screenshot)
        else:
            if warning:
                Report.logWarning(f"{attribute}{fail}displayed")
            else:
                Report.logFail(f"{attribute}{fail}displayed")