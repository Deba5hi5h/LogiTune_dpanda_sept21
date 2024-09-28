import unittest

from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class MultipleDevices(UIBase):
    sync_methods = SyncTCMethods()

    def test_2301_VC_69204_camera_settings_rallybar_rallybarmini(self):
        device_list = ["Rally Bar", "Rally Bar Mini"]
        for device in device_list:
            disconnect_device(device)
        self.sync_methods.tc_camera_settings_multiple_devices(device_names=device_list)

    def test_2302_VC_69943_camera_settings_rallycamera_meetup(self):
        device_list = ["Rally Camera", "MeetUp"]
        for device in device_list:
            disconnect_device(device)
        self.sync_methods.tc_camera_settings_multiple_devices(device_names=device_list)

    def test_2303_VC_69935_camera_settings_rally_rallycamera(self):
        device_list = ["Rally", "Rally Camera"]
        for device in device_list:
            disconnect_device(device)
        self.sync_methods.tc_camera_settings_multiple_devices(device_names=device_list)


if __name__ == "__main__":
    unittest.main()
