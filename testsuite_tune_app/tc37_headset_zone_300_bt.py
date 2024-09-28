import os
import platform
import unittest
import socket

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.usb_switch import disconnect_all
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_300_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType, DeviceName
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_300 import \
    ZONE_300_PROFILES
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_300


class Zone300BT(UIBase):
    """
    Test class containing UI tests scenarios for Zone 300 headset.
    """
    device_name = zone_300.device_name
    ota_api_product_name = zone_300.ota_api_product_name
    baseline_device_version = zone_300.baseline_device_version
    target_device_version = zone_300.target_device_version
    repeats = zone_300.repeats
    S3_FOLDER = "Logitech_Zone_300"

    conn_type = ConnectionType.bt
    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device_mac = zone_300_api.headset_bt_address
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    @classmethod
    def setUpClass(cls) -> None:
        """
        setUp: disconnect all devices on USB hub to avoid headset connect to dongle
        """
        super(Zone300BT, cls).setUpClass()
        disconnect_all()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tune_methods.set_never_sleep_timer_ui(product_string=cls.device_name)
        cls.tune_methods.tc_set_default_device_name(device_name=cls.device_name)
        cls.tune_methods.tc_bt_unpair_headset(device_mac=cls.device_mac, device_name=cls.device_name)

        super(Zone300BT, cls).tearDownClass()

    # TODO
    def prepare_update_items(self):
        file_path_headset = os.path.join(
            self.DIR_PATH, f"ZoneVibe125_Headset_{self.baseline_device_version}.img"
        )

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

    def test_3701_VC_123114_connect_headset_zone_300(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_bt_pair_headset(device_name=self.device_name, device_mac=self.device_mac)

        self.tune_methods.tc_bt_connect_headset(device_name=self.device_name, is_wireless=True)

    def test_3702_VC_123115_firmware_update_headset_zone_300(
            self) -> None:
        """
        Test method to verify firmware update.
        """
        self.skipTest("Feature not ready")
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_3703_VC_123116_sidetone_headset_zone_300(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """

        self.tune_methods.tc_bt_spp_sidetone(device_name=self.device_name,
                                             conn_type=self.conn_type)

    def test_3704_VC_123117_mic_level_zone_300(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.tune_methods.tc_mic_level(device_name=self.device_name)

    def test_3705_VC_123118_equalizer_headset_zone_300(self) -> None:
        """
        Test method to modify and verify and Equalizer feature.
        """
        self.tune_methods.tc_bt_spp_wireless_headset_equalizer(device_name=self.device_name,
                                                               conn_type=self.conn_type,
                                                               profiles=ZONE_300_PROFILES)

    def test_3706_VC_123119_rotate_to_mute_headset_zone_300(self) -> None:
        """
        Test method to modify and verify Rotate to mute feature.
        """
        self.tune_methods.tc_bt_spp_rotate_to_mute(device_name=self.device_name,
                                                   conn_type=self.conn_type)

    def test_3707_VC_123120_enable_voice_prompts_to_mute_headset_zone_300(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_bt_spp_voice_prompts(device_name=self.device_name,
                                                  conn_type=self.conn_type)

    def test_3708_VC_123121_device_name_zone_300(
            self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = 30
        self.tune_methods.tc_bt_spp_device_name(device_name=self.device_name,
                                                conn_type=self.conn_type,
                                                name_max_len=name_max_len)

    def test_3709_VC_123122_sleep_timeout_zone_300(
            self) -> None:
        """
        Test method to modify and verify Sleep timeout feature.
        """
        self.tune_methods.tc_bt_spp_sleep_settings(device_name=self.device_name,
                                                   conn_type=self.conn_type)

    def test_3710_VC_123123_connected_devices_zone_300(
            self) -> None:
        """
        Test method to verify Connection priority feature.
        """
        if get_custom_platform() == 'windows':
            receiver_name = os.environ['COMPUTERNAME']
        else:  # macOS
            # Mac M1
            if 'arm' in platform.processor():
                receiver_name = socket.gethostname().replace(".local", "").replace("sslaptop.logitech.com", "").upper()
                receiver_name = ("-".join(receiver_name[i:i + 2] for i in range(0, len(receiver_name), 2)))
            else:
                receiver_name = socket.gethostname().replace(".local", "").replace("ss-mbp.logitech.com", "").upper()
        self.tune_methods.tc_connected_devices(device_name=self.device_name,
                                               conn_type=self.conn_type,
                                               receiver_name=receiver_name)

    def test_3711_VC_123125_headset_language_zone_300(
            self) -> None:
        """
        Test method change and verify headset language feature.
        """
        self.skipTest("Feature not ready")
        test_name = unittest.TestCase.id(self).split('.')[-1]
        self.tune_methods.tc_language_update(device_name=self.device_name, test_name=test_name)

    def test_3712_VC_123126_headset_diagnostics_zone_300(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)

    def test_3713_VC_123127_about_the_headset_to_mute_headset_zone_300(
            self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
