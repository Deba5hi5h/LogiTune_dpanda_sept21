import os
import unittest

from typing import Optional

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import disconnect_device, disconnect_all
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zaxxon import \
    ZONE_TRUE_WIRELESS_EQ_PROFILES, MAX_LEN_NAME #ZONE_WIRELESS_BUTTONS_ACTIONS


class ZoneTrueWireless(UIBase):
    """
    Test class containing UI tests scenarios for Zone True Wireless headset.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import \
            is_acroname_available, zone_true_wireless
        tune_env = zone_true_wireless.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import \
            tune_env, is_acroname_available, zone_true_wireless

    device_name = zone_true_wireless.device_name
    ota_api_product_name = zone_true_wireless.ota_api_product_name
    baseline_device_version = zone_true_wireless.baseline_device_version
    baseline_dongle_version = zone_true_wireless.baseline_dongle_version
    target_device_version = zone_true_wireless.target_device_version
    target_dongle_version = zone_true_wireless.target_dongle_version
    dongle_address = zone_true_wireless.dongle_address
    repeats = zone_true_wireless.repeats
    S3_FOLDER = "Logitech_Zaxxon/files"
    conn_type = ConnectionType.dongle

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    @classmethod
    def setUpClass(cls) -> None:
        """
        setUp: disconnect all devices on USB hub to avoid headset connect to dongle
        """
        super(ZoneTrueWireless, cls).setUpClass()
        disconnect_all()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tune_methods.set_never_sleep_timer(product_string=cls.device_name, conn_type=cls.conn_type)
        cls.tune_methods.tc_set_default_device_name(device_name=cls.device_name)
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(ZoneTrueWireless, cls).tearDownClass()

    def prepare_update_items(self, dongle_type: Optional[str] = ''):
        file_path_headset = os.path.join(
            self.DIR_PATH, f"Zaxxon_v00.00.0{self.baseline_device_version}_encrypted_ota.bin"
        )
        if dongle_type.upper() == 'SUC':
            file_path_dongle = os.path.join(
                self.DIR_PATH, f"ZAXXON_SUC_{self.baseline_dongle_version}.dfu"
            )
        else:
            file_path_dongle = os.path.join(
                self.DIR_PATH, f"ZAXXON_BTC_{self.baseline_dongle_version}.dfu"
            )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(self.S3_FOLDER, file_path_headset, file_path_dongle)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            baseline_version_receiver=self.baseline_dongle_version,
            target_version_device=self.target_device_version,
            target_version_receiver=self.target_dongle_version,
            file_path_device=file_path_headset,
            file_path_receiver=file_path_dongle,
            tune_env=self.tune_env,
            timeout=1000,
            jenkins_configuration=JENKINS_FWU_CONFIG,
        )

        return fw_update, file_path_headset, file_path_dongle

    def test_3501_VC_103744_connect_headset_zone_true_wireless(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_connect_headset(device_name=self.device_name, is_wireless=True)

    def test_3502_VC_103745_firmware_update_headset_zone_true_wireless(self) -> None:
        """
        Test method to verify firmware update.
        """
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_3503_VC_103747_equalizer_headset_zone_true_wireless(self) -> None:
        """
        Test method to modify and verify and Equalizer feature.
        """
        self.tune_methods.tc_wireless_headset_equalizer(device_name=self.device_name,
                                                        conn_type=self.conn_type,
                                                        profiles=ZONE_TRUE_WIRELESS_EQ_PROFILES)

    def test_3504_VC_103748_enable_voice_prompts_to_mute_headset_zone_true_wireless(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_voice_prompts(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_3505_VC_103749_device_name_zone_true_wireless(self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = MAX_LEN_NAME
        self.tune_methods.tc_device_name(device_name=self.device_name,
                                         conn_type=self.conn_type,
                                         name_max_len=name_max_len)

    def test_3506_VC_103750_sleep_timeout_zone_true_wireless(self) -> None:
        """
        Test method to modify and verify Sleep timeout feature.
        """
        self.tune_methods.tc_sleep_settings(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_3507_VC_103751_connected_devices_zone_true_wireless(self) -> None:
        """
        Test method to verify Connection priority feature.
        """
        receiver_name = "Zone True Wireless Dongle"
        self.tune_methods.tc_connected_devices(device_name=self.device_name,
                                               conn_type=self.conn_type,
                                               receiver_name=receiver_name)

    def test_3508_VC_103752_buttons_functions_zone_true_wireless(self) -> None:
        """
        Test method change and verify Buttons functions feature.
        """
        self.skipTest("Cannot apply current function")
        self.tune_methods.tc_button_functions(device_name=self.device_name,
                                              conn_type=self.conn_type,
                                              button_actions=ZONE_WIRELESS_BUTTONS_ACTIONS)

    def test_3509_VC_103753_in_ear_detection_zone_true_wireless(self) -> None:
        """
        Test method change and verify In-ear detection feature.
        """
        self.tune_methods.tc_in_ear_detection(device_name=self.device_name, conn_type=self.conn_type)

    def test_3510_VC_103754_enable_receiver_connection_zone_true_wireless(self) -> None:
        """
        Test method change and verify Enable Receiver Connection feature.
        """
        self.skipTest("Need new tune_ui_method to verify")

    def test_3511_VC_103756_about_the_headset_to_mute_headset_zone_true_wireless(self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_3512_VC_103755_headset_diagnostics_zone_true_wireless(self) -> None:
        """
        Test method to verify headset diagnostics.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
