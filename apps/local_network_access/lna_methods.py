import time

from apps.browser_methods import BrowserClass
from apps.local_network_access.lna_home import LNAHome
from apps.local_network_access.lna_login import LNALogin
from base.base_ui import UIBase
from extentreport.report import Report


class LNAMethods(UIBase):
    """
    LNA test methods
    """
    home = LNAHome()
    browser = BrowserClass()

    def login_to_local_network_access(self, ip_address: str, user_name: str, password: str) -> LNAHome:
        """
        Method to log in to Local Network Access

        :param ip_address:
        :param password:
        :param user_name:

        :return: LNAHome
        """
        login = LNALogin()
        self.browser.close_all_browsers()
        self.browser.open_browser(f"https://{ip_address}/", browser="firefox")
        return login.login(user_name=user_name, password=password)

    def login_to_local_network_access_and_connect_to_sync(self, ip_address: str, user_name: str, password: str,
                                                          provision_code: str, seat_count: int = None,
                                                          device_name: str = None):
        """
        Method to log in to Local Network Access

        :param seat_count:
        :param provision_code:
        :param ip_address:
        :param password:
        :param user_name:

        :return:
        """
        sync_page = self.login_to_local_network_access(ip_address=ip_address, user_name=user_name, password=password) \
            .click_sync()
        self.browser.refresh()
        i = 0
        while i < 10:
            self.home.click_sync()
            if sync_page.verify_connect_to_sync_button_displayed():
                break
            i += 1
            self.browser.refresh()
            time.sleep(2)
        sync_page.click_connect_to_sync().type_in_provision_code(provision_code=provision_code).click_continue()

        if device_name is None:
            if seat_count is None:
                sync_page.click_skip_this_step()
            else:
                sync_page.type_in_seat_count(seat_count=str(seat_count)).click_submit()
        i = 0
        while i < 10:
            if sync_page.verify_disconnect_from_sync_button_displayed():
                break
            i += 1
            time.sleep(1)
        if sync_page.verify_disconnect_from_sync_button_displayed():
            Report.logPass("Device connected to Sync", True)
        else:
            Report.logFail("Device not connected to Sync")
        self.browser.close_browser()
