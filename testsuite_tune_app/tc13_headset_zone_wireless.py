import os
import time
import unittest

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.headset.headset_ui_methods import TuneHeadsetMethods, TuneHeadsetPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import disconnect_device
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zonewireless import \
    ZONE_WIRELESS_BUTTONS_ACTIONS, ZONE_WIRELESS_EQ_PROFILES


class ZoneWireless(UIBase):
    """
    Test class containing UI tests scenarios for Zone Wireless headset.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins \
            import is_acroname_available, zone_wireless
        tune_env = zone_wireless.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters \
            import tune_env, is_acroname_available, zone_wireless

    device_name = zone_wireless.device_name
    ota_api_product_name = zone_wireless.ota_api_product_name
    baseline_device_version = zone_wireless.baseline_device_version
    baseline_dongle_version = zone_wireless.baseline_dongle_version
    target_device_version = zone_wireless.target_device_version
    target_dongle_version = zone_wireless.target_dongle_version
    repeats = zone_wireless.repeats
    S3_FOLDER = "Logitech_Zone_Wireless"
    conn_type = ConnectionType.dongle

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device = TuneHeadsetMethods(device_name, tune_app)
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            cls.tune_methods.set_never_sleep_timer(product_string=cls.device_name, conn_type=cls.conn_type)
            time.sleep(3)
            cls.tune_methods.set_device_name_over_api(product_string=cls.device_name, conn_type=cls.conn_type)
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(ZoneWireless, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_headset = os.path.join(
            self.DIR_PATH, f"zonewireless_headset_{self.baseline_device_version}.bin")
        file_path_dongle = os.path.join(
            self.DIR_PATH, f"zonewireless_dongle_btc_{self.baseline_dongle_version}.dfu")

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
            jenkins_configuration=JENKINS_FWU_CONFIG,
        )

        return fw_update, file_path_headset, file_path_dongle

    def _back_button_universal_click(self) -> None:
        """
        Method that checks what back button is used in current view and click
        """
        if self.tune_app.verify_back_button_cybermorph():
            self.tune_app.click_back_button_cybermorph()
        elif self.tune_app.verify_back_to_device():
            self.tune_app.click_back_to_device()
        elif self.tune_app.verify_button_functions_back():
            self.tune_app.click_button_functions_back()

    def test_1301_VC_74078_connect_headset_zone_wireless(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_connect_headset(device_name=self.device_name, is_wireless=True)

    def test_1302_VC_74079_firmware_update_headset_zone_wireless(self) -> None:
        """
        Test method to verify firmware update.
        """
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_1303_VC_74080_sidetone_headset_zone_wireless(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """
        self.device.tc_sidetone(self.conn_type)

    def test_1304_VC_74085_mic_level_zone_wireless(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.device.tc_mic_level()

    def test_1305_VC_74086_noise_cancellation_zone_wireless(self) -> None:
        """
        Test method to modify and verify Noise cancellation feature.
        """
        self.tune_methods.tc_noise_cancellation(device_name=self.device_name,
                                                conn_type=self.conn_type)

    def test_1306_VC_74087_check_default_presets_values_zone_wireless(self) -> None:
        """
        Test to verify default equalizer preset's values.
        """
        self.device.tc_equalizer_check_default_presets_values()

    def test_1307_VC_112783_add_and_delete_custom_presets_zone_wireless(self) -> None:
        """
        Test to verify if adding and deleting custom presets works correctly.
        """
        self.device.tc_equalizer_add_and_delete_custom_presets()

    def test_1308_VC_112784_check_max_presets_prompt_zone_wireless(self) -> None:
        """
        Test to verify if max presets prompt occurs.
        """
        self.device.tc_equalizer_check_max_custom_presets_prompt()

    def test_3209_VC_112785_max_preset_name_input_zone_wireless(self):
        """
        Test to verify maximum length of custom equalizer preset name.
        """
        self.device.tc_equalizer_max_preset_name_length()

    def test_1310_VC_74081_rotate_to_mute_headset_zone_wireless(self) -> None:
        """
        Test method to modify and verify Rotate to mute feature.
        """
        self.tune_methods.tc_rotate_to_mute(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_1311_VC_74082_enable_voice_prompts_to_mute_headset_zone_wireless(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_voice_prompts(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_1312_VC_74088_device_name_zone_wireless(self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = 30
        self.tune_methods.tc_device_name(device_name=self.device_name,
                                         conn_type=self.conn_type,
                                         name_max_len=name_max_len)

    def test_1313_VC_74091_sleep_timeout_zone_wireless(self) -> None:
        """
        Test method to modify and verify Sleep timeout feature.
        """
        self.tune_methods.tc_sleep_settings(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_1314_VC_74093_connection_priority_zone_wireless(self) -> None:
        """
        Test method to modify and verify Connection priority feature.
        """
        self.tune_methods.tc_connection_priority(device_name=self.device_name)

    def test_1315_VC_74095_connected_devices_zone_wireless(self) -> None:
        """
        Test method to verify Connection priority feature.
        """
        receiver_name = "Zone Wireless Receiver"
        self.tune_methods.tc_connected_devices(device_name=self.device_name,
                                               conn_type=self.conn_type,
                                               receiver_name=receiver_name)

    def test_1316_VC_74098_buttons_functions_zone_wireless(self) -> None:
        """
        Test method change and verify Buttons functions feature.
        """
        self.tune_methods.tc_button_functions(device_name=self.device_name,
                                              conn_type=self.conn_type,
                                              button_actions=ZONE_WIRELESS_BUTTONS_ACTIONS)

    def test_1317_VC_74097_headset_language_zone_wireless(self) -> None:
        """
        Test method change and verify headset language feature.
        """
        test_name = unittest.TestCase.id(self).split('.')[-1]
        self.tune_methods.tc_language_update(device_name=self.device_name, test_name=test_name)

    def test_1318_VC_103457_headset_diagnostics_zone_wireless(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)

    def test_1319_VC_74083_about_the_headset_to_mute_headset_zone_wireless(self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_1320_VC_112537_parameters_persistency_after_reconnect_zone_wireless(self) -> None:
        """
        Test to verify parameters persistency after reconnecting headset.
        """
        head_persist = TuneHeadsetPersistency(headset_name=self.device_name, tune_app=self.tune_app)
        head_persist.check_persistency(acroname_automatic=self.is_acroname_available)


if __name__ == "__main__":
    unittest.main()
