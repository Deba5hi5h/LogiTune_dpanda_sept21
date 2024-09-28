import os
import random
import unittest
import platform
import socket

from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType, DeviceName
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_wireless_2 import \
    MAX_LEN_NAME, ZONE_WIRELESS_2_PROFILES
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wireless_2_api

directory = os.path.dirname(os.path.dirname(__file__))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")


class ZoneWireless2(UIBase):
    """
    Test class containing UI tests scenarios for Zone Wireless 2 headset.
    """
    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device_name = DeviceName.zone_wireless_2
    conn_type = ConnectionType.bt
    device_mac = zone_wireless_2_api.headset_bt_address

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tune_methods.bt_spp_set_never_sleep_timer(product_string=cls.device_name,
                                                      conn_type=cls.conn_type)
        cls.tune_methods.tc_set_default_device_name(device_name=cls.device_name)
        cls.tune_methods.tc_bt_unpair_headset(device_mac=cls.device_mac, device_name=cls.device_name)
        super(ZoneWireless2, cls).tearDownClass()
    
    def test_3301_VC_103721_connect_headset_zone_wireless_2(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_bt_pair_headset(device_name=self.device_name, device_mac=self.device_mac)
        self.tune_methods.tc_bt_connect_headset(device_name=self.device_name, is_wireless=True)

    def test_3302_VC_103722_firmware_update_headset_zone_wireless_2(
            self) -> None:
        """
        Test method to verify firmware update.
        """
        Report.logSkip("Feature not ready.")
        self.skipTest("Feature not ready.")

    def test_3303_VC_103723_anc_levels_zone_wireless_2(self) -> None:
        """
        Test method to modify parameters and verify ANC feature.
        """
        self.tune_methods.tc_anc_buttons(device_name=self.device_name,
                                      conn_type=self.conn_type)

    def test_3304_VC_103724_sidetone_headset_zone_wireless_2(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """
        self.tune_methods.tc_bt_spp_sidetone(device_name=self.device_name,
                                      conn_type=self.conn_type)

    def test_3305_VC_103725_mic_level_zone_wireless_2(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.tune_methods.tc_mic_level(device_name=self.device_name)

    def test_3306_VC_103726_advanced_call_clarity_zone_wireless_2(
            self) -> None:
        """
        Test method to modify and verify Advanced Call Clarity feature.
        """
        self.tune_methods.tc_advanced_call_clarity(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_3307_VC_103727_equalizer_headset_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify and Equalizer feature.
        """
        self.tune_methods.tc_bt_spp_wireless_headset_equalizer(device_name=self.device_name,
                                                        conn_type=self.conn_type,
                                                        profiles=ZONE_WIRELESS_2_PROFILES)

    def test_3308_VC_103728_health_and_safety_anti_startle_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify Health and Safety feature.
        """
        self.tune_methods.tc_health_and_safety_anti_startle(device_name=self.device_name,
                                         conn_type=self.conn_type)

    def test_3309_VC_103743_health_and_safety_noise_exposure_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify Health and Safety feature.
        """
        self.tune_methods.tc_health_and_safety_noise_exposure(device_name=self.device_name,
                                         conn_type=self.conn_type)

    def test_3310_VC_103729_device_name_zone_wireless_2(
            self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = MAX_LEN_NAME
        self.tune_methods.tc_bt_spp_device_name(device_name=self.device_name,
                                         conn_type=self.conn_type,
                                         name_max_len=name_max_len)

    def test_3311_VC_103730_sleep_timeout_zone_wireless_2(
            self) -> None:
        """
        Test method to modify and verify Sleep timeout feature.
        """
        self.tune_methods.tc_bt_spp_sleep_settings(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_3312_VC_103731_rotate_to_mute_headset_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify Rotate to mute feature.
        """
        self.tune_methods.tc_bt_spp_rotate_to_mute(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_3313_VC_103732_anc_button_options_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify ANC button options feature.
        """
        self.tune_methods.tc_anc_button_options(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_3314_VC_103733_on_head_detection_auto_mute_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify On Head detection: Auto Mute feature.
        """
        self.tune_methods.tc_on_head_detection_auto_mute(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_3315_VC_103734_on_head_detection_auto_answer_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify On Head detection: Auto Answer feature.
        """
        self.tune_methods.tc_on_head_detection_auto_answer(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_3316_VC_103735_on_head_detection_auto_pause_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify On Head detection: Auto pause feature.
        """
        self.tune_methods.tc_on_head_detection_auto_pause(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_3317_VC_103736_voice_prompts_headset_zone_wireless_2(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_voice_prompts_3_levels(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_3318_VC_103737_connected_devices_zone_wireless_2(
            self) -> None:
        """
        Test method to verify Connection priority feature.
        """
        """
                Test method to verify Connection priority feature.
                """
        if get_custom_platform() == 'windows':
            receiver_name = os.environ['COMPUTERNAME']
        else:
            # Mac M1
            if 'arm' in platform.processor():
                receiver_name = socket.gethostname().replace(".local", "").replace("sslaptop.logitech.com", "").upper()
                receiver_name = ("-".join(receiver_name[i:i + 2] for i in range(0, len(receiver_name), 2)))
            else:
                receiver_name = socket.gethostname().replace(".local", "").replace("ss-mbp.logitech.com", "").upper()
        self.tune_methods.tc_connected_devices(device_name=self.device_name,
                                               conn_type=self.conn_type,
                                               receiver_name=receiver_name)

    def test_3319_VC_103738_headset_language_zone_wireless_2(
            self) -> None:
        """
        Test method change and verify headset language feature.
        """
        self.tune_methods.tc_cybermorph_language_selection(device_name=self.device_name)

    def test_3320_VC_103740_headset_diagnostics_zone_wireless_2(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)

    def test_3321_VC_103741_about_the_headset_to_mute_headset_zone_wireless_2(
            self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_3322_VC_103742_factory_reset_to_mute_zone_wireless_2(
            self) -> None:
        """
        Test method to verify Factory Reset feature.
        """
        Report.logSkip("TBD")
        self.skipTest("TBD")


if __name__ == "__main__":
    unittest.main()
