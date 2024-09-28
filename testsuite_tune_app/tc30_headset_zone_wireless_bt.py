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
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wireless_api
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zonewireless import \
    ZONE_WIRELESS_EQ_PROFILES, ZONE_WIRELESS_BUTTONS_ACTIONS
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_wireless


class ZoneWirelessBT(UIBase):
    """
    Test class containing UI tests scenarios for Zone wireless headset.
    """
    device_name = zone_wireless.device_name
    ota_api_product_name = zone_wireless.ota_api_product_name
    baseline_device_version = zone_wireless.baseline_device_version
    target_device_version = zone_wireless.target_device_version
    repeats = zone_wireless.repeats
    S3_FOLDER = "Logitech_Zone_Wireless"

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    conn_type = ConnectionType.bt_ui
    device_mac = zone_wireless_api.headset_bt_address
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    @classmethod
    def setUpClass(cls) -> None:
        """
        setUp: disconnect all devices on USB hub to avoid headset connect to dongle
        """
        super(ZoneWirelessBT, cls).setUpClass()
        disconnect_all()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tune_methods.tc_set_default_device_name(device_name=cls.device_name)
        cls.tune_methods.set_never_sleep_timer_ui(product_string=cls.device_name)
        cls.tune_methods.tc_bt_unpair_headset(device_mac=cls.device_mac, device_name=cls.device_name)

        super(ZoneWirelessBT, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_headset = os.path.join(
            self.DIR_PATH, f"zonewireless_headset_{self.baseline_device_version}.bin")

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


    def test_3001_VC_103544_connect_headset_zone_wireless(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_bt_pair_headset(device_name=self.device_name, device_mac=self.device_mac)

        self.tune_methods.tc_bt_connect_headset(device_name=self.device_name, is_wireless=True)

    def test_3002_VC_103545_firmware_update_headset_zone_wireless(
            self) -> None:
        """
        Test method to verify firmware update.
        """
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_3003_VC_103546_sidetone_headset_zone_wireless(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """

        self.tune_methods.tc_bt_spp_sidetone(device_name=self.device_name,
                                             conn_type=self.conn_type)

    def test_3004_VC_103547_mic_level_zone_wireless(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.tune_methods.tc_mic_level(device_name=self.device_name)

    def test_3005_VC_103549_equalizer_headset_zone_wireless(self) -> None:
        """
        Test method to modify and verify and Equalizer feature.
        """
        self.tune_methods.tc_bt_spp_wireless_headset_equalizer(device_name=self.device_name,
                                                               conn_type=self.conn_type,
                                                           profiles=ZONE_WIRELESS_EQ_PROFILES)

    def test_3006_VC_103550_rotate_to_mute_headset_zone_wireless(self) -> None:
        """
        Test method to modify and verify Rotate to mute feature.
        """
        self.tune_methods.tc_bt_spp_rotate_to_mute(device_name=self.device_name,
                                                   conn_type=self.conn_type)

    def test_3007_VC_103551_enable_voice_prompts_to_mute_headset_zone_wireless(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_bt_spp_voice_prompts(device_name=self.device_name,
                                                  conn_type=self.conn_type)

    def test_3008_VC_103553_sleep_timeout_zone_wireless(
            self) -> None:
        """
        Test method to modify and verify Sleep timeout feature.
        """
        self.tune_methods.tc_bt_spp_sleep_settings(device_name=self.device_name,
                                                   conn_type=self.conn_type)

    def test_3009_VC_103555_connected_devices_zone_wireless(
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

    def test_3010_VC_103557_headset_language_zone_wireless(
            self) -> None:
        """
        Test method change and verify headset language feature.
        """
        test_name = unittest.TestCase.id(self).split('.')[-1]
        self.tune_methods.tc_language_update(device_name=self.device_name, test_name=test_name)

    def test_3011_VC_103559_about_the_headset_to_mute_headset_zone_wireless(
            self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_3012_VC_103556_buttons_functions_zone_wireless(self) -> None:
        """
        Test method change and verify Buttons functions feature.
        """
        self.tune_methods.tc_bt_spp_button_functions(device_name=self.device_name,
                                                     conn_type=self.conn_type,
                                              button_actions=ZONE_WIRELESS_BUTTONS_ACTIONS)

    def test_3013_VC_103554_connection_priority_zone_wireless(self) -> None:
        """
        Test method to modify and verify Connection priority feature.
        """
        self.tune_methods.tc_connection_priority(device_name=self.device_name)

    def test_3014_VC_103548_noise_cancellation_zone_wireless(self) -> None:
        """
        Test method to modify and verify Noise cancellation feature.
        """
        self.tune_methods.tc_bt_spp_noise_cancellation(device_name=self.device_name,
                                                       conn_type=self.conn_type)

    def test_3015_VC_103552_device_name_zone_wireless(
            self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = 30
        self.tune_methods.tc_bt_spp_device_name(device_name=self.device_name,
                                                conn_type=self.conn_type,
                                                name_max_len=name_max_len)

    def test_3016_VC_103558_headset_diagnostics_zone_wireless(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
