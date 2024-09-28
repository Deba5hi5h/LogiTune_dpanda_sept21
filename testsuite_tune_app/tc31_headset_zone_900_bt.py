import os
import unittest
import socket
import platform

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.usb_switch import disconnect_all
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType, DeviceName
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_900_api
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone900 import \
    ZONE_900_BUTTONS_ACTIONS, ZONE_900_EQ_PROFILES
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_900



class Zone900BT(UIBase):
    """
    Test class containing UI tests scenarios for Zone 900 headset.
    """
    device_name = zone_900.device_name
    ota_api_product_name = zone_900.ota_api_product_name
    baseline_device_version = zone_900.baseline_device_version
    target_device_version = zone_900.target_device_version
    repeats = zone_900.repeats
    S3_FOLDER = "Logitech_Zone_900"

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    conn_type = ConnectionType.bt_ui
    device_mac = zone_900_api.headset_bt_address
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    @classmethod
    def setUpClass(cls) -> None:
        """
        setUp: disconnect all devices on USB hub to avoid headset connect to dongle
        """
        super(Zone900BT, cls).setUpClass()
        disconnect_all()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tune_methods.set_never_sleep_timer_ui(product_string=cls.device_name)
        cls.tune_methods.tc_set_default_device_name(device_name=cls.device_name)
        cls.tune_methods.tc_bt_unpair_headset(device_mac=cls.device_mac, device_name=cls.device_name)

        super(Zone900BT, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_headset = os.path.join(
            self.DIR_PATH, f"zone900_headset_{self.baseline_device_version}.bin")

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(self.S3_FOLDER, file_path_headset)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            target_version_device=self.target_device_version,
            file_path_device=file_path_headset,
            tune_env=tune_env,
        )

        return fw_update, file_path_headset

    def test_3101_VC_103560_connect_headset_zone_900(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_bt_pair_headset(device_name=self.device_name, device_mac=self.device_mac)

        self.tune_methods.tc_bt_connect_headset(device_name=self.device_name, is_wireless=True)

    def test_3102_VC_103561_firmware_update_headset_zone_900(
            self) -> None:
        """
        Test method to verify firmware update.
        """
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_3103_VC_103562_sidetone_headset_zone_900(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """

        self.tune_methods.tc_bt_spp_sidetone(device_name=self.device_name,
                                             conn_type=self.conn_type)

    def test_3104_VC_103564_mic_level_zone_900(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.tune_methods.tc_mic_level(device_name=self.device_name)

    def test_3105_VC_103566_equalizer_headset_zone_900(self) -> None:
        """
        Test method to modify and verify and Equalizer feature.
        """
        self.tune_methods.tc_bt_spp_wireless_headset_equalizer(device_name=self.device_name,
                                                               conn_type=self.conn_type,
                                                               profiles=ZONE_900_EQ_PROFILES)

    def test_3106_VC_103563_rotate_to_mute_headset_zone_900(self) -> None:
        """
        Test method to modify and verify Rotate to mute feature.
        """
        self.tune_methods.tc_bt_spp_rotate_to_mute(device_name=self.device_name,
                                                   conn_type=self.conn_type)

    def test_3107_VC_103567_enable_voice_prompts_to_mute_headset_zone_900(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_bt_spp_voice_prompts(device_name=self.device_name,
                                                  conn_type=self.conn_type)

    def test_3108_VC_103569_sleep_timeout_zone_900(
            self) -> None:
        """
        Test method to modify and verify Sleep timeout feature.
        """
        self.tune_methods.tc_bt_spp_sleep_settings(device_name=self.device_name,
                                                   conn_type=self.conn_type)

    def test_3109_VC_103571_connected_devices_zone_900(
            self) -> None:
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

    def test_3110_VC_103573_headset_language_zone_900(
            self) -> None:
        """
        Test method change and verify headset language feature.
        """
        test_name = unittest.TestCase.id(self).split('.')[-1]
        self.tune_methods.tc_language_update(device_name=self.device_name, test_name=test_name)

    def test_3111_VC_103575_about_the_headset_to_mute_headset_zone_900(
            self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_3112_VC_103572_buttons_functions_zone_900(self) -> None:
        """
        Test method change and verify Buttons functions feature.
        """
        self.tune_methods.tc_bt_spp_button_functions(device_name=self.device_name,
                                                     conn_type=self.conn_type,
                                              button_actions=ZONE_900_BUTTONS_ACTIONS)

    def test_3113_VC_103570_connection_priority_zone_900(self) -> None:
        """
        Test method to modify and verify Connection priority feature.
        """
        self.tune_methods.tc_connection_priority(device_name=self.device_name)

    def test_3114_VC_103565_noise_cancellation_zone_900(self) -> None:
        """
        Test method to modify and verify Noise cancellation feature.
        """
        self.tune_methods.tc_bt_spp_noise_cancellation(device_name=self.device_name,
                                                       conn_type=self.conn_type)

    def test_3115_VC_103568_device_name_zone_900(
            self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = 30
        self.tune_methods.tc_bt_spp_device_name(device_name=self.device_name,
                                                conn_type=self.conn_type,
                                                name_max_len=name_max_len)

    def test_3116_VC_103574_headset_diagnostics_zone_900(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()