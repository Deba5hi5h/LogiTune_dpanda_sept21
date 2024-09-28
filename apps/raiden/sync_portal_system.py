import time

from apps.raiden.sync_portal_users import SyncPortalUsers
from base.base_ui import UIBase
from locators.sync_portal.sync_portal_system_locators import SyncPortalSystemLocators


class SyncPortalSystem(UIBase):

    def click_users_tab(self):
        """
        Method to click on Users tab

        :param :
        :return : SyncPortalHome
        """
        self.look_element(SyncPortalSystemLocators.USERS_TAB).click()
        return SyncPortalUsers()
