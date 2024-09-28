import unittest

from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class Celestia(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Scribe"

    def test_701_VC_39953_celestia_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_702_VC_40641_celestia_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_703_VC_40006_celestia_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_704_VC_40053_celestia_video_tab(self):
        self.sync_methods.tc_scribe_video_tab(device_name=self.device_name)

    def test_705_VC_39959_celestia_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_706_VC_40090_celestia_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_707_VC_39995_celestia_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_708_VC_44291_celestia_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)

        
if __name__ == "__main__":
    unittest.main()
