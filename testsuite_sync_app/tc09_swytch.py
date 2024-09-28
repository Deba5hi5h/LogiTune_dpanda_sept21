import unittest

from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class Swytch(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Swytch"

    def test_901_VC_39977_swytch_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_902_VC_56317_swytch_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_903_VC_40013_swytch_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_904_VC_39992_swytch_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_905_VC_40091_swytch_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_906_VC_40001_swytch_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_907_VC_56318_swytch_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)

if __name__ == "__main__":
    unittest.main()
