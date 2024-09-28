import time
from datetime import datetime

from apps.browser_methods import BrowserClass
from apps.local_network_access.lna_sync_app_methods import LNASyncAppMethods
from apps.raiden.raiden_config.raiden_config import RaidenConfig
from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.raiden.sync_portal_dashboard_meeting_rooms import SyncPortalDashboardMeetingRooms
from apps.raiden.sync_portal_home import SyncPortalHome
from apps.raiden.sync_portal_inventory import SyncPortalInventory
from apps.raiden.sync_portal_login import SyncPortalLogin
from apps.raiden.sync_portal_methods import SyncPortalMethods
from apps.raiden.sync_portal_room import SyncPortalRoom
from apps.sync.sync_app_methods import SyncAppMethods
from base import global_variables
from base.base_ui import UIBase
from common.ipswitch_helper import IPSwitchHelper
from extentreport.report import Report
from testsuite_sync_app.tc_methods import SyncTCMethods


class SyncPortalTests(SyncPortalMethods):
    browser = BrowserClass()
    raiden = SyncPortalMethods()
    sync_portal = SyncPortalAppMethods()
    lna = LNASyncAppMethods()
    sync_methods = SyncTCMethods()
    sync_app = SyncAppMethods()
    home = SyncPortalHome()
    dashboard_meeting_rooms = SyncPortalDashboardMeetingRooms()
    login = SyncPortalLogin()

    def tc_login_to_sync_portal(self):
        role = "AladdinOwner" if global_variables.SYNC_ENV == "raiden-prod" else "OrgAdmin"
        self.raiden.login_to_sync_portal(config=global_variables.config, role=role)
        if self.inventory.verify_search_box_displayed():
            Report.logPass("Successful login to Sync Portal", screenshot=True)
        else:
            Report.logFail("Sync Portal login not successful")

    def tc_logout_from_sync_portal(self):
        if self.raiden.logout_from_sync_portal():
            Report.logPass("Successful logout from Sync Portal", screenshot=True)
        else:
            Report.logFail("Did not logout from Sync Portal successfully")
        global_variables.driver.quit()

    def tc_sync_portal_navigation(self):
        verification = self.home.click_meeting_rooms_dashboard().verify_meeting_dashboard_page()
        self.report_displayed_or_not("Meeting Rooms - Dashboard page", verification)
        time.sleep(1)
        verification = self.home.click_meeting_rooms_issues().verify_meeting_rooms_issues_page()
        self.report_displayed_or_not("Meeting Rooms - Issues page", verification)
        if global_variables.SYNC_ENV == 'raiden-prod':
            time.sleep(1)
            verification = self.home.click_flex_desks_dashboard().verify_flex_desks_dashboard_page()
            self.report_displayed_or_not("Flex Desks - Dashboard page", verification)
            time.sleep(1)
            verification = self.home.click_flex_desks_issues().verify_flex_desks_issues_page()
            self.report_displayed_or_not("Flex Desks - Issues page", verification)

    def tc_install_sync_desktop_app(self):
        self.sync_methods.tc_install_sync_app()
        if self.sync_app.open().click_room().verify_room_disconnected():
            Report.logPass("Room not connected on skip setup")
        else:
            Report.logPass("Connect to room not displayed on skip setup")

    def tc_provision_room_using_credentials(self):
        room_name = self.sync_methods.tc_connect_to_sync_portal(close_browser=False)
        inventory = SyncPortalInventory()
        use_state = ''
        for _ in range(5):
            use_state = inventory.get_room_use_state(room_name=room_name)
            if str(use_state).lower() != 'unknown':
                break
            time.sleep(2)
            self.browser.refresh()
        self.report_displayed_or_not("Use state 'Available'", use_state.lower() == "available")

    def tc_delete_room_from_sync_portal(self):
        room_name = self.sync_app.open().get_room_name()
        self.sync_app.close()
        self.sync_portal.login_to_sync_portal_and_delete_room(config=global_variables.config,
                                                              role=global_variables.SYNC_ROLE,
                                                              room_name=room_name)
        if self.sync_app.open().click_room().verify_room_disconnected():
            Report.logPass(f"Room {room_name} is disconnected from Sync App", True)
        else:
            Report.logFail(f"Room {room_name} is not disconnected from Sync App")
        self.sync_app.close()

    def tc_landing_page(self):
        self.browser.open_browser(global_variables.config.BASE_URL)
        self.report_displayed_or_not("Username field", self.login.verify_user_name())
        self.report_displayed_or_not("Password field", self.login.verify_password())
        self.report_displayed_or_not("Login button", self.login.verify_login_page())
        self.browser.close_browser()
        self.browser.open_browser(f"{global_variables.config.BASE_URL}/api/version")
        api_info = self.login.get_api_information()
        Report.logInfo(f"API Information - {api_info}")
        self.browser.close_browser()

    def tc_provision_device_disconnect_reconnect(self, device_name: str):
        ip_address = RaidenConfig.get_ip_address(device_name=device_name)
        user_name = RaidenConfig.get_user_name(device_name=device_name)
        password = RaidenConfig.get_password(device_name=device_name)
        power_port = RaidenConfig.get_power_port(device_name=device_name)
        now = datetime.now()
        room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Raiden"
        provision_code = self.sync_portal.create_empty_room_and_get_provision_code(room_name=room_name)
        self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=ip_address,
                                                                   user_name=user_name,
                                                                   password=password,
                                                                   provision_code=provision_code,
                                                                   seat_count=10)
        self.sync_portal.verify_device_added_in_sync_portal(device_name=device_name, room_name=room_name,
                                                            close_browser=False)
        time.sleep(5)
        self.room.click_close_button()
        use_state = self.inventory.get_room_use_state(room_name=room_name)
        self.report_displayed_or_not("Use state 'Available'", use_state.lower() == "available")
        IPSwitchHelper.switch_off(device_name=power_port)
        Report.logInfo(f"Turning off device - {device_name}")
        for _ in range(120):
            self.browser.refresh()
            time.sleep(2)
            use_state = self.inventory.get_room_use_state(room_name=room_name)
            if use_state.lower() == "offline":
                IPSwitchHelper.switch_on(device_name=power_port)
                break
        self.report_displayed_or_not("Use state 'Error'", use_state.lower() == "offline")
        Report.logInfo(f"Turning on device - {device_name}")
        for _ in range(120):
            self.browser.refresh()
            time.sleep(2)
            use_state = self.inventory.get_room_use_state(room_name=room_name)
            if use_state.lower() == "available":
                break
        self.report_displayed_or_not("Use state 'Available'", use_state.lower() == "available")
        self.browser.close_browser()
        self.sync_portal.login_to_sync_portal_and_delete_room(config=global_variables.config,
                                                              role=global_variables.SYNC_ROLE,
                                                              room_name=room_name)