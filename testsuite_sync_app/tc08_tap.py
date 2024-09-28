import unittest

from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class Tap(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Tap"

    def test_801_VC_39976_tap_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_802_VC_40646_tap_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_803_VC_40012_tap_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_804_VC_39991_tap_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_805_VC_40612_tap_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_806_VC_40000_tap_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_807_VC_44294_tap_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)

if __name__ == "__main__":
    unittest.main()
