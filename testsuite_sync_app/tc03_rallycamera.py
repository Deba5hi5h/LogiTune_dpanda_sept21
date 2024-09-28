import unittest
from unittest import SkipTest

from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.sync.Firmware import Firmware
from common.platform_helper import get_custom_platform
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *

class RallyCamera(UIBase):
    sync_methods = SyncTCMethods()
    sync_portal = SyncPortalAppMethods()
    device_name = "Rally Camera"

    def test_301_VC_40086_rallycamera_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_303_VC_40644_rallycamera_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_302_VC_40065_rallycamera_video_tab(self):
        self.sync_methods.tc_video_tab(device_name=self.device_name)

    def test_304_VC_40017_rallycamera_rightsight_options(self):
        self.sync_methods.tc_rightsight_in_sync(device_name=self.device_name)

    def test_305_VC_39980_rallycamera_update_firmware(self):
        global_variables.retry_test = False
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        rallycamera = Firmware(device_name=self.device_name)
        rallycamera.downgrade_firmware()
        self.sync_methods.tc_compare_syncapp_device_info_to_syncportal(device_name=self.device_name, update=True)
        self.sync_methods.tc_update_firmware(self.device_name)

    def test_306_VC_40071_rallycamera_landing_page(self):
        self.sync_methods.tc_landing_page(device_name=self.device_name)
        self.sync_methods.tc_compare_syncapp_device_info_to_syncportal(device_name=self.device_name)

    def test_307_VC_40010_rallycamera_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_308_VC_69950_rallycamera_camera_manual_color_settings_in_sync(self):
        self.sync_methods.tc_manual_color_settings_in_sync(device_name=self.device_name)

    def test_309_VC_69956_rallycamera_camera_settings_another_video_application(self):
        self.sync_methods.tc_camera_settings_stream_in_google_meet(device_name=self.device_name)

    def test_310_VC_69954_rallycamera_camera_settings_grid_mode(self):
        self.sync_methods.tc_camera_settings_grid_mode(device_name=self.device_name)

    def test_311_VC_70885_rallycamera_camera_settings_forget_device(self):
        global_variables.retry_test = False
        self.sync_methods.tc_camera_settings_forget_and_reconnect_device(device_name=self.device_name)

    def test_312_VC_69953_rallycamera_camera_settings_floating_window(self):
        self.sync_methods.tc_camera_settings_floating_window(device_name=self.device_name)

    def test_313_VC_69955_rallycamera_camera_manual_color_settings_unplug_replug(self):
        global_variables.retry_test = False
        self.sync_methods.tc_manual_color_settings_unplug_replug_in_sync(device_name=self.device_name)

    def test_314_VC_69949_rallycamera_camera_settings_adjustments(self):
        self.sync_methods.tc_camera_adjustments(device_name=self.device_name)

    def test_315_VC_39989_rallycamera_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_316_VC_39974_rallycamera_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_317_VC_39998_rallycamera_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_318_VC_44293_rallycamera_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
