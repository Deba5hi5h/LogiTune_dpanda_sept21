import unittest
from unittest import SkipTest

from apps.sync.middleware_log import MiddlewareLog
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class SyncAppCollabOS(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Rally Bar"

    def setUp(self) -> None:
        global_variables.testStatus = "Pass"
        testName = self.__getattribute__("_testMethodName")
        global_variables.reportInstance = global_variables.extent.createTest(f"{testName}_{self.device_name}",
                                                                             "Test Case Details")

    def test_101_VC_XXXX_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_102_VC_XXXX_rightsight2(self):
        if self.device_name == "Rally Bar Huddle":
            self.sync_methods.tc_rightsight_in_sync(device_name=self.device_name)
        else:
            self.sync_methods.tc_rightsight2_in_sync(device_name=self.device_name)

    def test_103_VC_XXXX_groupview_speakerview_persistence(self):
        if self.device_name == "Rally Bar Huddle":
            Report.logSkip("Test Case not supported for Rally bar huddle")
            raise SkipTest("Test Case not supported for Rally bar huddle")
        self.sync_methods.tc_speakerview_groupview_in_sync(device_name=self.device_name)

    def test_104_VC_XXXX_antiflicker_settings(self):
        self.sync_methods.tc_anti_flicker_in_sync(device_name=self.device_name)

    def test_105_VC_XXXX_audio_speaker_boost(self):
        if self.device_name == "Rally Bar Huddle":
            Report.logSkip("Test Case not supported for Rally bar huddle")
            raise SkipTest("Test Case not supported for Rally bar huddle")
        self.sync_methods.tc_audio_speaker_boost(device_name=self.device_name)

    def test_106_VC_XXXX_audio_ai_noise_suppression(self):
        self.sync_methods.tc_audio_ai_noise_suppression(device_name=self.device_name)

    def test_107_VC_XXXX_audio_reverb_control_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_reverb_control_device(device_name=self.device_name)

    def test_108_VC_XXXX_audio_speaker_eq_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_speaker_eq_device(device_name=self.device_name)

    def test_109_VC_XXXX_manual_color_settings_in_sync(self):
        self.sync_methods.tc_manual_color_settings_in_sync(device_name=self.device_name)

    def test_110_VC_XXXX_camera_settings_floating_window(self):
        self.sync_methods.tc_camera_settings_floating_window(device_name=self.device_name)

    def test_111_VC_XXXX_camera_settings_adjustments(self):
        self.sync_methods.tc_camera_adjustments(device_name=self.device_name)

    def test_112_VC_XXXX_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
