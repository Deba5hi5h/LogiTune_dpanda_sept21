from datetime import datetime
import unittest

from apps.browser_methods import BrowserClass
from apps.local_network_access.lna_sync_app_methods import LNASyncAppMethods
from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.sync.AppInstall import AppInstall
from apps.sync.middleware_log import MiddlewareLog
from apps.sync.sync_app_methods import SyncAppMethods
from base import global_variables
from common.framework_params import INSTALLER
from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_all
from config.aws_helper import AWSHelper
from extentreport.report import Report
from locators.win_ui_locators import SyncAppLocators
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase


class ProvisionCode(UIBase):
    sync_methods = SyncTCMethods()
    sync_portal = SyncPortalAppMethods()
    lna = LNASyncAppMethods()
    sync_app = SyncAppMethods()
    room_name = None

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.SYNC_ENV = 'raiden-prod'
        global_variables.config = AWSHelper.get_config(global_variables.SYNC_ENV)
        super(ProvisionCode, cls).setUpClass()

    def test_2801_VC_74479_fre_provision_code_setup(self):
        now = datetime.now()
        self.room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-" + get_custom_platform()
        disconnect_all()
        app = AppInstall()
        if get_custom_platform() == "windows":
            app.uninstallApp()
            app.installApp()
        else:
            app.uninstall_sync_mac()
            app.install_sync_mac(INSTALLER)
        provision_code = self.sync_portal.create_empty_room_and_get_provision_code(room_name=self.room_name)
        self.sync_app.open(fre=True)
        self.sync_app.setup.click_get_started()
        if self.sync_app.room.click_room_provision_code().type_in_provision_code(provision_code) \
                .click_connect_room().verify_room_connected():
            Report.logPass("Room connected to Sync Portal successfully", True)
        else:
            Report.logFail("Room connect to Sync Portal Failed")
        self.sync_app.close()
        self.sync_methods.tc_add_device("MeetUp")
        self._delete_room(room_name=self.room_name)

    def test_2802_VC_74481_provision_code_multiple_hosts(self):
        room_name = "QA-MTR-CR"
        provision_code = self.sync_portal.get_provision_code_from_existing_room(room_name=room_name)
        self.sync_app.open()
        self.sync_app.verify_provision_code_multiple_hosts_error(provision_code=provision_code).close()

    def test_2803_VC_74482_provision_incorrect_code(self):
        provision_code = "111100001111"
        self.sync_app.open()
        self.sync_app.verify_incorrect_provision_code_error(provision_code=provision_code).close()

    def test_2804_VC_74480_provision_code_connect_now(self):
        device_name = "Rally Bar"
        now = datetime.now()
        type(self).room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-" + get_custom_platform()
        provision_code = self.sync_portal.create_empty_room_and_get_provision_code(room_name=self.room_name)
        self.sync_app.open()
        self.sync_app.connect_to_sync_portal_using_provision_code(provision_code=provision_code).close()
        self.sync_methods.tc_add_device(device_name)
        self.sync_app.open()
        self.sync_app.forget_problem_device(device_name=device_name).close()

    def test_2805_VC_74483_provision_code_delete_room_from_sync_portal(self):
        if self.room_name is not None:
            self._delete_room(room_name=self.room_name)

    def test_2806_VC_74485_provision_code_collabos_device_appliance_mode(self):
        browser = BrowserClass()
        browser.close_all_browsers()
        device_name = "Rally Bar"
        self.sync_app.open()
        self.sync_app.add_device_pnp(device_name=device_name).forget_problem_device(device_name=device_name).close()
        now = datetime.now()
        type(self).room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-" + get_custom_platform()
        provision_code = self.sync_portal.create_empty_room_and_get_provision_code(room_name=self.room_name)
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(device_name)
        self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=self.sync_methods.lna_ip,
                                                                   user_name=self.sync_methods.lna_user,
                                                                   password=self.sync_methods.lna_pass,
                                                                   provision_code=provision_code, seat_count=10)
        self.sync_portal.verify_device_added_in_sync_portal(device_name=device_name, room_name=self.room_name)
        self.sync_app.open()
        self.sync_app.verify_provision_code_multiple_hosts_error(provision_code=provision_code).close()
        self._delete_room(room_name=self.room_name)

    def test_2807_VC_74484_provision_code_existing_room(self):
        device_name = "Tap Scheduler"
        now = datetime.now()
        type(self).room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-" + get_custom_platform()
        provision_code = self.sync_portal.create_empty_room_and_get_provision_code(room_name=self.room_name)
        self.sync_methods.lna_ip = "172.28.78.159"
        self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=self.sync_methods.lna_ip,
                                                                   user_name=self.sync_methods.lna_user,
                                                                   password=self.sync_methods.lna_pass,
                                                                   provision_code=provision_code, seat_count=10)
        self.sync_portal.verify_device_added_in_sync_portal(device_name=device_name, room_name=self.room_name)
        self.sync_app.open()
        self.sync_app.connect_to_sync_portal_using_provision_code(provision_code=provision_code).close()
        self._delete_room(room_name=self.room_name)

    def _delete_room(self, room_name) -> None:
        self.sync_portal.login_to_sync_portal_and_delete_room(config=global_variables.config,
                                                              role=global_variables.SYNC_ROLE,
                                                              room_name=room_name)
        if self.sync_app.open().click_room().verify_room_disconnected():
            Report.logPass(f"Room {room_name} is disconnected from Sync App", True)
        else:
            Report.logFail(f"Room {room_name} is not disconnected from Sync App")
        self.sync_app.close()


if __name__ == "__main__":
    unittest.main()
