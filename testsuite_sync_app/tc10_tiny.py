import unittest

from apps.sync.middleware_log import MiddlewareLog
from common.platform_helper import get_custom_platform
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class Tiny(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Rally Bar Huddle"

    @classmethod
    def setUpClass(cls) -> None:
        cls.sync_methods.sync_app.restart_sync_services()
        super(Tiny, cls).setUpClass()

    def test_1001_VC_94140_rallybarhuddle_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_1002_VC_118959_rallybarhuddle_camera_tab(self):
        self.sync_methods.tc_video_tab(device_name=self.device_name)

    def test_1003_VC_118960_rallybarhuddle_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_1004_VC_96294_rallybarhuddle_rightsight_in_sync(self):
        self.sync_methods.tc_rightsight_in_sync(device_name=self.device_name)

    def test_1005_VC_118965_rallybarhuddle_audio_tab(self):
        self.sync_methods.tc_audio_tab(device_name=self.device_name)

    def test_1006_VC_94144_rallybarhuddle_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_1007_VC_96286_rallybarhuddle_antiflicker_settings(self):
        self.sync_methods.tc_anti_flicker_in_sync(device_name=self.device_name)

    def test_1008_VC_96287_rallybarhuddle_bluetooth_options(self):
        self.sync_methods.tc_bluetooth_in_sync(device_name=self.device_name)

    def test_1009_VC_120433_rallybarhuddle_bluetooth_options_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_bluetooth_device_in_sync(device_name=self.device_name)

    def test_1010_VC_96289_rallybarhuddle_audio_ai_noise_suppression(self):
        self.sync_methods.tc_audio_ai_noise_suppression(device_name=self.device_name)

    def test_1011_VC_120432_rallybarhuddle_audio_ai_noise_suppression_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_ai_noise_suppression_device(device_name=self.device_name)

    def test_1012_VC_96290_rallybarhuddle_audio_reverb_control(self):
        self.sync_methods.tc_audio_reverb_control(device_name=self.device_name)

    def test_1013_VC_120434_rallybarhuddle_audio_reverb_control_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_reverb_control_device(device_name=self.device_name)

    def test_1014_VC_96291_rallybarhuddle_audio_microphone_eq(self):
        self.sync_methods.tc_audio_microphone_eq(device_name=self.device_name)

    def test_1015_VC_120435_rallybarhuddle_audio_microphone_eq_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_microphone_eq_device(device_name=self.device_name)

    def test_1016_VC_96292_rallybarhuddle_audio_speaker_eq(self):
        self.sync_methods.tc_audio_speaker_eq(device_name=self.device_name)

    def test_1017_VC_120438_rallybarhuddle_audio_speaker_eq_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_speaker_eq_device(device_name=self.device_name)

    def test_1018_VC_96284_rallybarhuddle_manual_color_settings_in_sync(self):
        self.sync_methods.tc_manual_color_settings_in_sync(device_name=self.device_name)

    def test_1019_VC_120441_rallybarhuddle_camera_settings_another_video_application(self):
        self.sync_methods.tc_camera_settings_stream_in_google_meet(device_name=self.device_name)

    def test_1020_VC_120442_rallybarhuddle_camera_settings_grid_mode(self):
        self.sync_methods.tc_camera_settings_grid_mode(device_name=self.device_name)

    def test_1021_VC_120443_rallybarhuddle_camera_settings_forget_device(self):
        if get_custom_platform() != "windows":
            global_variables.retry_test = False
        self.sync_methods.tc_camera_settings_forget_and_reconnect_device(device_name=self.device_name)

    def test_1022_VC_120445_rallybarhuddle_camera_settings_floating_window(self):
        self.sync_methods.tc_camera_settings_floating_window(device_name=self.device_name)

    def test_1023_VC_120446_rallybarhuddle_manual_color_settings_unplug_replug(self):
        if get_custom_platform() != "windows":
            global_variables.retry_test = False
        self.sync_methods.tc_manual_color_settings_unplug_replug_in_sync(device_name=self.device_name)

    def test_1024_VC_96285_rallybarhuddle_camera_settings_adjustments(self):
        self.sync_methods.tc_camera_adjustments(device_name=self.device_name)

    def test_1025_VC_94142_rallybarhuddle_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_1026_VC_94141_rallybarhuddle_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_1027_VC_94143_rallybarhuddle_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_1028_VC_118970_rallybarhuddle_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)

if __name__ == "__main__":
    unittest.main()
