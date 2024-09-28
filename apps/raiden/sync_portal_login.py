from apps.raiden.sync_portal_inventory import SyncPortalInventory
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_portal.sync_portal_inventory_locators import SyncPortalInventoryLocators
from locators.sync_portal.sync_portal_login_locators import SyncPortalLoginLocators


class SyncPortalLogin(UIBase):
    """
    Login Page UI test helper methods
    """

    def login(self, config: str, role: str):
        """
        Method to log in Sync Portal

        :param config:
        :param role:
        :return: SyncPortalInventory
        """
        try:
            email = config.ROLES[role]['signin_payload']['email']
            pwd = config.ROLES[role]['signin_payload']['password']

            username = self.look_element(SyncPortalLoginLocators.USERNAME)
            username.send_keys(email)
            password = self.look_element(SyncPortalLoginLocators.PASSWORD)
            password.send_keys(pwd)
            login = self.look_element(SyncPortalLoginLocators.LOGIN)
            login.click()
            UIBase.highlight_flag = False
            self.verify_element(SyncPortalInventoryLocators.SEARCH_BOX)
            return SyncPortalInventory()
        except Exception as e:
            Report.logException(str(e))
            raise e

    def verify_login_page(self) -> bool:
        """
        Method to verify Sync Portal Login page

        :param :
        :return: bool
        """
        return self.verify_element(SyncPortalLoginLocators.LOGIN)

    def verify_user_name(self) -> bool:
        """
        Method to verify username field displayed

        :param :
        :return: bool
        """
        return self.verify_element(SyncPortalLoginLocators.USERNAME)

    def verify_password(self) -> bool:
        """
        Method to verify password field displayed

        :param :
        :return: bool
        """
        return self.verify_element(SyncPortalLoginLocators.PASSWORD)

    def get_api_information(self) -> str:
        """
        Method to get API information

        :param :
        :return: bool
        """
        return self.look_element(SyncPortalLoginLocators.API).text

