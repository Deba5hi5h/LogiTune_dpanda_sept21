import unittest

from apis.sync_helper import SyncHelper
from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.sync.AppInstall import AppInstall
from apps.sync.sync_app_methods import SyncAppMethods
from base.base_ui import UIBase
from common.framework_params import INSTALLER
from common.usb_switch import disconnect_all
from common.system_info import *
from testsuite_sync_app.tc_methods import SyncTCMethods


class Install(UIBase):
    sync_methods = SyncTCMethods()
    sync_app = SyncAppMethods()
    sync_portal = SyncPortalAppMethods()

    def test_001_VC_39949_install_sync_app(self):
        self.sync_methods.tc_install_sync_app()

    def test_002_VC_39971_connect_to_sync_portal(self):
        self.sync_methods.tc_connect_to_sync_portal()

    def test_003_VC_130978_room_information(self):
        room_name = self.sync_app.open_and_get_room_name()
        try:
            def compare_values(param_name: str, param1: str, param2: str, app: str = "App"):
                if param1.upper() in param2.upper():
                    Report.logPass(f"{param_name} displayed in Sync {app} is correct - {param1}")
                else:
                    Report.logFail(f"{param_name} displayed in Sync {app} is incorrect - {param2} vs {param1}")

            sync_version = SyncHelper.get_logisync_version()
            sync_info = self.sync_app.get_room_information()
            [sys_computer_type, sys_operating_system, sys_os_version, sys_memory] = SystemInfo.get_system_info()
            compare_values("Computer Type", sys_computer_type, sync_info["computer_type"])
            compare_values("Operating System", sys_operating_system, sync_info["operating_system"])
            compare_values("OS Version", sys_os_version, sync_info["os_version"])
            compare_values("Memory", sys_memory, sync_info["memory"])
            room_info = self.sync_portal.get_room_information(room_name=room_name)
            compare_values("Sync App version", room_info["sync_app_version"], sync_version, "Portal")
            compare_values("Computer Type", room_info["computer_type"], sync_info["computer_type"], "Portal")
            compare_values("Operating System", room_info["operating_system"], sync_info["operating_system"], "Portal")
            compare_values("OS Version", room_info["os_version"], sync_info["os_version"], "Portal")
            compare_values("Memory", room_info["memory"], str(sync_info["memory"]).replace(".00", ""), "Portal")
        except Exception as e:
            Report.logException(str(e))
        self.sync_app.close()


if __name__ == "__main__":
    unittest.main()
