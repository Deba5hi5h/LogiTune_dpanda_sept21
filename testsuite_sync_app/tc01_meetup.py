import unittest
from unittest import SkipTest

from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.sync.Firmware import Firmware
from apps.sync.sync_app_methods import SyncAppMethods
from common.platform_helper import get_custom_platform
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class Meetup(UIBase):
    sync_methods = SyncTCMethods()
    sync_portal = SyncPortalAppMethods()
    device_name = "MeetUp"

    def test_101_VC_39972_meetup_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_102_VC_40642_meetup_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_103_VC_40063_meetup_video_tab(self):
        self.sync_methods.tc_video_tab(device_name=self.device_name)

    def test_104_VC_40015_meet_up_rightsight_in_sync(self):
        self.sync_methods.tc_rightsight_in_sync(device_name=self.device_name)

    def test_105_VC_40092_interrupt_firmware_update(self):
        global_variables.retry_test = False
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        meetup = Firmware(device_name=self.device_name)
        meetup.downgrade_firmware()
        self.sync_methods.tc_compare_syncapp_device_info_to_syncportal(device_name=self.device_name, update=True)
        self.sync_methods.tc_update_firmware_interrupt(self.device_name)

    def test_106_VC_39978_update_firmware(self):
        global_variables.retry_test = False
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        self.sync_methods.tc_update_firmware(self.device_name)

    def test_107_VC_40069_meet_up_landing_page(self):
        self.sync_methods.tc_landing_page(device_name=self.device_name)
        self.sync_methods.tc_compare_syncapp_device_info_to_syncportal(device_name=self.device_name)

    def test_108_VC_40060_meetup_audio_tab(self):
        self.sync_methods.tc_audio_tab(device_name=self.device_name)

    def test_109_VC_40008_meetup_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_110_VC_69941_meet_up_manual_color_settings_in_sync(self):
        self.sync_methods.tc_manual_color_settings_in_sync(device_name=self.device_name)

    def test_111_VC_69948_meetup_camera_settings_another_video_application(self):
        self.sync_methods.tc_camera_settings_stream_in_google_meet(device_name=self.device_name)

    def test_112_VC_69947_meet_up_manual_color_settings_unplug_replug(self):
        global_variables.retry_test = False
        self.sync_methods.tc_manual_color_settings_unplug_replug_in_sync(device_name=self.device_name)

    def test_113_VC_69946_meetup_camera_settings_grid_mode(self):
        self.sync_methods.tc_camera_settings_grid_mode(device_name=self.device_name)

    def test_114_VC_70884_meetup_camera_settings_forget_device(self):
        global_variables.retry_test = False
        self.sync_methods.tc_camera_settings_forget_and_reconnect_device(device_name=self.device_name)

    def test_115_VC_69945_meetup_camera_settings_floating_window(self):
        self.sync_methods.tc_camera_settings_floating_window(device_name=self.device_name)

    def test_116_VC_69940_meetup_camera_settings_adjustments(self):
        self.sync_methods.tc_camera_adjustments(device_name=self.device_name)

    def test_117_VC_39987_meetup_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_118_VC_40084_meetup_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_119_VC_39996_meetup_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_120_VC_44287_meetup_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
