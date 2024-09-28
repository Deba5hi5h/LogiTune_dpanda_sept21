import time

from base.base_ui import UIBase
from locators.sync_portal.sync_portal_users_locators import SyncPortalUsersLocators


class SyncPortalUsers(UIBase):

    def click_on_it_users(self):
        """
        Method to click on IT Users tab

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.IT_USERS).click()
        return SyncPortalUsers()

    def click_on_end_users(self):
        """
        Method to click on End Users tab

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.END_USERS).click()
        return SyncPortalUsers()

    def click_on_user_checkbox(self, user: str):
        """
        Method to click on checkbox next to user

        :param : user (User Email ID, First Name or Last Name)
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.USER_CHECKBOX, param=user).click()
        return SyncPortalUsers()

    def click_on_modify_groups(self):
        """
        Method to click on Modify Groups

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.MODIFY_GROUPS).click()
        return SyncPortalUsers()

    def click_on_user_group_dropdown(self):
        """
        Method to click on user groups dropdown

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.USER_GROUPS_DROPDOWN).click()
        return SyncPortalUsers()

    def click_on_user_groups_main_screen(self):
        """
        Method to click on user groups dropdown from End Users home screen

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.USER_GROUPS_MAIN).click()
        return SyncPortalUsers()

    def click_on_user_group_selection(self, user_group):
        """
        Method to click on User Group selection

        :param : user_group
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.USER_GROUP_SELECTION, param=user_group).click()
        return SyncPortalUsers()

    def click_on_confirm(self):
        """
        Method to click on Confirm button

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.CONFIRM).click()
        return SyncPortalUsers()

    def click_on_search_result(self, search_result: str):
        """
        Method to click on text displayed in search results

        :param :search_result
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.SEARCH_RESULT, param=search_result).click()
        return SyncPortalUsers()

    def click_on_change_role(self):
        """
        Method to click on change button

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.ROLE_CHANGE).click()
        return SyncPortalUsers()

    def click_on_role_dropdown(self):
        """
        Method to click on role dropdown

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.ROLE_DROPDOWN).click()
        return SyncPortalUsers()

    def click_save(self):
        """
        Method to click on Save button

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.ROLE_SAVE).click()
        return SyncPortalUsers()

    def click_apply(self):
        """
        Method to click on Apply button

        :param :
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.APPLY).click()
        return SyncPortalUsers()

    def type_in_search(self, search_text: str):
        """
        Method to click on Users tab

        :param :search_text
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.SEARCH).send_keys(search_text)
        return SyncPortalUsers()

    def select_role(self, role: str):
        """
        Method to select role from dropdwon

        :param :role
        :return :SyncPortalUsers
        """
        self.look_element(SyncPortalUsersLocators.ROLE_SELECT, param=role).click()
        return SyncPortalUsers()

    def get_current_user_groups_for_user(self) -> str:
        """
        Method to get list of current associated user groups (String separated by comma)

        :param :
        :return :SyncPortalUsers
        """
        try:
            user_groups = self.look_element(SyncPortalUsersLocators.USER_GROUPS_TEXTBOX)
            return user_groups.text
        except:
            return ""

    def verify_user_group_updated_message(self) -> bool:
        """
        Method to verify User Group updated message

        :param :
        :return :bool
        """
        return self.verify_element(SyncPortalUsersLocators.USER_GROUP_SUCCESS_MESSAGE)

    def get_current_user_groups_added(self):
        """
        Method to get list of current user groups added

        :param :
        :return :user_groups
        """
        user_groups = []
        try:
            groups = self.look_all_elements(SyncPortalUsersLocators.USER_GROUPS_MAIN_ITEMS)
            for group in groups:
                user_groups.append(group.text)
        except Exception as e:
            pass
        return user_groups

    def get_user_count_for_user_group(self, user_group: str) -> int:
        """
        Method to get list of current user groups added

        :param :
        :return :user_count
        """
        user_count = 0
        try:
            user_group = self.look_element(SyncPortalUsersLocators.USER_GROUP_COUNT, param=user_group)
            user_count = int(user_group.text)
        except Exception as e:
            pass
        return user_count
