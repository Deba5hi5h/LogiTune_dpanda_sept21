import unittest

from apps.sync.middleware_log import MiddlewareLog
from common.platform_helper import get_custom_platform
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class Kong(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Rally Bar"

    @classmethod
    def setUpClass(cls) -> None:
        cls.sync_methods.sync_app.restart_sync_services()
        super(Kong, cls).setUpClass()

    def test_401_VC_39951_rallybar_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_402_VC_40066_rallybar_video_tab(self):
        self.sync_methods.tc_video_tab(device_name=self.device_name)

    def test_403_VC_40639_rallybar_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_404_VC_40019_rallybar_rightsight_options(self):
        self.sync_methods.tc_rightsight_in_sync(device_name=self.device_name)

    def test_405_VC_58626_rallybar_rightsight2(self):
        self.sync_methods.tc_rightsight2_in_sync(device_name=self.device_name)

    def test_406_VC_58627_rallybar_rightsight2_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_rightsight2_device_in_sync(device_name=self.device_name)

    def test_407_VC_66922_rallybar_speakerview(self):
        self.sync_methods.tc_speakerview_in_sync(device_name=self.device_name)

    def test_408_VC_66920_rallybar_groupview(self):
        self.sync_methods.tc_groupview_in_sync(device_name=self.device_name)

    def test_409_VC_130980_rallybar_groupview_speakerview_persistence(self):
        self.sync_methods.tc_speakerview_groupview_in_sync(device_name=self.device_name)

    def test_410_VC_40117_rallybar_audio_tab(self):
        self.sync_methods.tc_audio_tab(device_name=self.device_name)

    def test_411_VC_40004_rallybar_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_412_VC_40029_rallybar_antiflicker_settings(self):
        self.sync_methods.tc_anti_flicker_in_sync(device_name=self.device_name)

    def test_413_VC_40031_rallybar_bluetooth_options(self):
        self.sync_methods.tc_bluetooth_in_sync(device_name=self.device_name)

    def test_414_VC_40033_rallybar_bluetooth_options_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_bluetooth_device_in_sync(device_name=self.device_name)

    def test_415_VC_40035_rallybar_audio_speaker_boost(self):
        self.sync_methods.tc_audio_speaker_boost(device_name=self.device_name)

    def test_416_VC_72040_rallybar_audio_speaker_boost_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_speaker_boost_device(device_name=self.device_name)

    def test_417_VC_40037_rallybar_audio_ai_noise_suppression(self):
        self.sync_methods.tc_audio_ai_noise_suppression(device_name=self.device_name)

    def test_418_VC_72046_rallybar_audio_ai_noise_suppression_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_ai_noise_suppression_device(device_name=self.device_name)

    def test_419_VC_40039_rallybar_audio_reverb_control(self):
        self.sync_methods.tc_audio_reverb_control(device_name=self.device_name)

    def test_420_VC_72050_rallybar_audio_reverb_control_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_reverb_control_device(device_name=self.device_name)

    def test_421_VC_53059_rallybar_audio_microphone_eq(self):
        self.sync_methods.tc_audio_microphone_eq(device_name=self.device_name)

    def test_422_VC_53060_rallybar_audio_microphone_eq_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_microphone_eq_device(device_name=self.device_name)

    def test_423_VC_53061_rallybar_audio_speaker_eq(self):
        self.sync_methods.tc_audio_speaker_eq(device_name=self.device_name)

    def test_424_VC_53062_rallybar_audio_speaker_eq_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_speaker_eq_device(device_name=self.device_name)

    def test_425_VC_69201_rallybar_manual_color_settings_in_sync(self):
        self.sync_methods.tc_manual_color_settings_in_sync(device_name=self.device_name)

    def test_426_VC_69210_rallybar_camera_settings_another_video_application(self):
        self.sync_methods.tc_camera_settings_stream_in_google_meet(device_name=self.device_name)

    def test_427_VC_69206_rallybar_camera_settings_grid_mode(self):
        self.sync_methods.tc_camera_settings_grid_mode(device_name=self.device_name)

    def test_428_VC_70880_rallybar_camera_settings_forget_device(self):
        if get_custom_platform() != "windows":
            global_variables.retry_test = False
        self.sync_methods.tc_camera_settings_forget_and_reconnect_device(device_name=self.device_name)

    def test_429_VC_69205_rallybar_camera_settings_floating_window(self):
        self.sync_methods.tc_camera_settings_floating_window(device_name=self.device_name)

    def test_430_VC_69209_rallybar_manual_color_settings_unplug_replug(self):
        if get_custom_platform() != "windows":
            global_variables.retry_test = False
        self.sync_methods.tc_manual_color_settings_unplug_replug_in_sync(device_name=self.device_name)

    def test_431_VC_69200_rallybar_camera_settings_adjustments(self):
        self.sync_methods.tc_camera_adjustments(device_name=self.device_name)

    def test_432_VC_39957_rallybar_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_433_VC_40088_rallybar_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_434_VC_39993_rallybar_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_435_VC_44289_rallybar_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
