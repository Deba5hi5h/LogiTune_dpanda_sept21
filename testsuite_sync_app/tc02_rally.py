import unittest
from unittest import SkipTest

from apps.sync.Firmware import Firmware
from common.platform_helper import get_custom_platform
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class Rally(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Rally"

    def test_201_VC_40085_rally_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_202_VC_40643_rally_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_203_VC_40064_rally_video_tab(self):
        self.sync_methods.tc_video_tab(device_name=self.device_name)

    def test_204_VC_40016_rally_rightsight_options(self):
        self.sync_methods.tc_rightsight_in_sync(device_name=self.device_name)

    def test_205_VC_39979_rally_update_firmware(self):
        global_variables.retry_test = False
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        rally = Firmware(device_name=self.device_name)
        rally.downgrade_firmware()
        self.sync_methods.tc_update_firmware(device_name=self.device_name)

    def test_206_VC_40061_rally_audio_tab(self):
        self.sync_methods.tc_audio_tab(device_name=self.device_name)

    def test_207_VC_40009_rally_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_208_VC_69931_rally_manual_color_settings_in_sync(self):
        self.sync_methods.tc_manual_color_settings_in_sync(device_name=self.device_name)

    def test_209_VC_69939_rally_camera_settings_another_video_application(self):
        self.sync_methods.tc_camera_settings_stream_in_google_meet(device_name=self.device_name)

    def test_210_VC_69938_rally_manual_color_settings_unplug_replug(self):
        global_variables.retry_test = False
        self.sync_methods.tc_manual_color_settings_unplug_replug_in_sync(device_name=self.device_name)

    def test_211_VC_69937_rally_camera_settings_grid_mode(self):
        self.sync_methods.tc_camera_settings_grid_mode(device_name=self.device_name)

    def test_212_VC_70883_rally_camera_settings_forget_device(self):
        global_variables.retry_test = False
        self.sync_methods.tc_camera_settings_forget_and_reconnect_device(device_name=self.device_name)

    def test_213_VC_69936_rally_camera_settings_floating_window(self):
        self.sync_methods.tc_camera_settings_floating_window(device_name=self.device_name)

    def test_214_VC_69928_rally_camera_settings_adjustments(self):
        self.sync_methods.tc_camera_adjustments(device_name=self.device_name)

    def test_215_VC_39988_rally_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_216_VC_39973_rally_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_217_VC_39997_rally_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_218_VC_44292_rally_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
