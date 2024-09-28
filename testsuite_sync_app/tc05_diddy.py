import unittest

from apps.sync.middleware_log import MiddlewareLog
from common.platform_helper import get_custom_platform
from common.usb_switch import *
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase


class Diddy(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Rally Bar Mini"

    @classmethod
    def setUpClass(cls) -> None:
        cls.sync_methods.sync_app.restart_sync_services()
        super(Diddy, cls).setUpClass()

    def test_501_VC_39952_rallybarmini_add_device(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device(device_name=self.device_name)

    def test_502_VC_40005_rallybarmini_device_detection(self):
        self.sync_methods.tc_device_detection(device_name=self.device_name)

    def test_503_VC_40640_rallybarmini_check_raiden_portal(self):
        self.sync_methods.tc_check_raiden_portal(device_name=self.device_name)

    def test_504_VC_40020_rallybarmini_rightsight_options(self):
        self.sync_methods.tc_rightsight_in_sync(device_name=self.device_name)

    def test_505_VC_58628_rallybarmini_rightsight2(self):
        self.sync_methods.tc_rightsight2_in_sync(device_name=self.device_name)

    def test_506_VC_58629_rallybarmini_rightsight2_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_rightsight2_device_in_sync(device_name=self.device_name)

    def test_507_VC_66926_rallybarmini_speakerview(self):
        self.sync_methods.tc_speakerview_in_sync(device_name=self.device_name)

    def test_508_VC_66924_rallybarmini_groupview(self):
        self.sync_methods.tc_groupview_in_sync(device_name=self.device_name)

    def test_509_VC_130981_rallybarmini_groupview_speakerview_persistence(self):
        self.sync_methods.tc_speakerview_groupview_in_sync(device_name=self.device_name)

    def test_510_VC_40062_rallybarmini_audio_tab(self):
        self.sync_methods.tc_audio_tab(device_name=self.device_name)

    def test_511_VC_40067_rallybarmini_video_tab(self):
        self.sync_methods.tc_video_tab(device_name=self.device_name)

    def test_512_VC_40030_rallybarmini_antiflicker_settings(self):
        self.sync_methods.tc_anti_flicker_in_sync(device_name=self.device_name)

    def test_513_VC_40032_rallybarmini_bluetooth_options(self):
        self.sync_methods.tc_bluetooth_in_sync(device_name=self.device_name)

    def test_514_VC_40034_rallybarmini_bluetooth_options_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_bluetooth_device_in_sync(device_name=self.device_name)

    def test_515_VC_40036_rallybarmini_audio_speaker_boost(self):
        self.sync_methods.tc_audio_speaker_boost(device_name=self.device_name)

    def test_516_VC_72041_rallybarmini_audio_speaker_boost_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_speaker_boost_device(device_name=self.device_name)

    def test_517_VC_40038_rallybarmini_audio_ai_noise_suppression(self):
        self.sync_methods.tc_audio_ai_noise_suppression(device_name=self.device_name)

    def test_518_VC_72049_rallybarmini_audio_ai_noise_suppression_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_ai_noise_suppression_device(device_name=self.device_name)

    def test_519_VC_40040_rallybarmini_audio_reverb_control(self):
        self.sync_methods.tc_audio_reverb_control(device_name=self.device_name)

    def test_520_VC_72051_rallybarmini_audio_reverb_control_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_reverb_control_device(device_name=self.device_name)

    def test_521_VC_53063_rallybarmini_audio_microphone_eq(self):
        self.sync_methods.tc_audio_microphone_eq(device_name=self.device_name)

    def test_522_VC_53064_rallybarmini_audio_microphone_eq_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_microphone_eq_device(device_name=self.device_name)

    def test_523_VC_53065_rallybarmini_audio_speaker_eq(self):
        self.sync_methods.tc_audio_speaker_eq(device_name=self.device_name)

    def test_524_VC_53066_rallybarmini_audio_speaker_eq_device(self):
        if self.sync_methods.lna_ip is None:
            self.sync_methods.lna_ip = MiddlewareLog.get_ip_address(self.device_name)
        self.sync_methods.tc_audio_speaker_eq_device(device_name=self.device_name)

    def test_525_VC_69214_rallybarmini_manual_color_settings(self):
        self.sync_methods.tc_manual_color_settings_in_sync(device_name=self.device_name)

    def test_526_VC_69222_rallybarmini_camera_settings_another_video_application(self):
        self.sync_methods.tc_camera_settings_stream_in_google_meet(device_name=self.device_name)

    def test_527_VC_69219_rallybarmini_camera_settings_grid_mode(self):
        self.sync_methods.tc_camera_settings_grid_mode(device_name=self.device_name)

    def test_528_VC_70882_rallybarmini_camera_settings_forget_device(self):
        if get_custom_platform() != "windows":
            global_variables.retry_test = False
        self.sync_methods.tc_camera_settings_forget_and_reconnect_device(device_name=self.device_name)

    def test_529_VC_69217_rallybarmini_camera_settings_floating_window(self):
        self.sync_methods.tc_camera_settings_floating_window(device_name=self.device_name)

    def test_530_VC_69213_rallybarmini_camera_settings_adjustments(self):
        self.sync_methods.tc_camera_adjustments(device_name=self.device_name)

    def test_531_VC_69221_rallybarmini_manual_color_settings_unplug_replug(self):
        if get_custom_platform() != "windows":
            global_variables.retry_test = False
        self.sync_methods.tc_manual_color_settings_unplug_replug_in_sync(device_name=self.device_name)

    def test_532_VC_39958_rallybarmini_forget_device(self):
        connect_device(device_name=self.device_name)
        self.sync_methods.tc_forget_device(device_name=self.device_name)

    def test_533_VC_40089_rallybarmini_add_device_pnp(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_add_device_pnp(device_name=self.device_name)

    def test_534_VC_39994_rallybarmini_forget_problem_device(self):
        self.sync_methods.tc_remove_problem_device(device_name=self.device_name)

    def test_535_VC_44290_rallybarmini_forget_problem_device_sync_portal(self):
        disconnect_device(device_name=self.device_name)
        self.sync_methods.tc_remove_problem_device_sync_portal(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
