import unittest

from apps.sync.middleware_log import MiddlewareLog
from common.platform_helper import get_custom_platform
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class Sentinel(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Sight"

    @classmethod
    def setUpClass(cls) -> None:
        cls.sync_methods.sync_app.restart_sync_services()
        super(Sentinel, cls).setUpClass()

    def test_1101_VC_93165_sight_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_1102_VC_120469_sight_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_1103_VC_93169_sight_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_1104_VC_93167_sight_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_1105_VC_93166_sight_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_1106_VC_93168_sight_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_1107_VC_120470_sight_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
